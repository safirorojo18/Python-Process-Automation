from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

COLORS = ["B", "Y", "R", "K", "W"]
COLOR_NAMES = {
    "B": "Azul",
    "Y": "Amarillo",
    "R": "Rojo",
    "K": "Negro",
    "W": "Blanco",
}

WALL_PATTERN = [
    ["B", "Y", "R", "K", "W"],
    ["W", "B", "Y", "R", "K"],
    ["K", "W", "B", "Y", "R"],
    ["R", "K", "W", "B", "Y"],
    ["Y", "R", "K", "W", "B"],
]

FLOOR_PENALTIES = [-1, -1, -2, -2, -2, -3, -3]


@dataclass
class Player:
    name: str
    score: int = 0
    pattern_lines: list[list[str]] = field(
        default_factory=lambda: [[] for _ in range(5)]
    )
    wall: list[list[bool]] = field(
        default_factory=lambda: [[False] * 5 for _ in range(5)]
    )
    floor: list[str] = field(default_factory=list)

    def wall_has_color_in_row(self, row: int, color: str) -> bool:
        col = WALL_PATTERN[row].index(color)
        return self.wall[row][col]

    def can_place_in_pattern_line(self, row: int, color: str) -> bool:
        line = self.pattern_lines[row]
        capacity = row + 1

        if self.wall_has_color_in_row(row, color):
            return False
        if line and line[0] != color:
            return False

        return len(line) < capacity

    def place_tiles(self, row: Optional[int], color: str, count: int) -> None:
        if row is None:
            self.floor.extend([color] * count)
            return

        capacity = row + 1
        available = capacity - len(self.pattern_lines[row])
        placed = min(count, available)
        overflow = count - placed

        self.pattern_lines[row].extend([color] * placed)
        self.floor.extend([color] * overflow)

    def score_tile(self, row: int, col: int) -> int:
        horizontal = 1
        c = col - 1
        while c >= 0 and self.wall[row][c]:
            horizontal += 1
            c -= 1

        c = col + 1
        while c < 5 and self.wall[row][c]:
            horizontal += 1
            c += 1

        vertical = 1
        r = row - 1
        while r >= 0 and self.wall[r][col]:
            vertical += 1
            r -= 1

        r = row + 1
        while r < 5 and self.wall[r][col]:
            vertical += 1
            r += 1

        if horizontal == 1 and vertical == 1:
            return 1
        if horizontal == 1:
            return vertical
        if vertical == 1:
            return horizontal

        return horizontal + vertical

    def finish_round(self) -> list[str]:
        discarded: list[str] = []

        for row in range(5):
            capacity = row + 1
            line = self.pattern_lines[row]

            if len(line) == capacity:
                color = line[0]
                col = WALL_PATTERN[row].index(color)
                self.wall[row][col] = True
                self.score += self.score_tile(row, col)

                discarded.extend(line[1:])
                self.pattern_lines[row] = []

        penalty = sum(FLOOR_PENALTIES[: min(len(self.floor), 7)])
        self.score = max(0, self.score + penalty)

        discarded.extend(tile for tile in self.floor if tile != "1")
        self.floor.clear()

        return discarded

    def has_complete_row(self) -> bool:
        return any(all(row) for row in self.wall)

    def add_end_game_bonuses(self) -> None:
        completed_rows = sum(all(row) for row in self.wall)
        self.score += completed_rows * 2

        completed_columns = 0
        for col in range(5):
            if all(self.wall[row][col] for row in range(5)):
                completed_columns += 1
        self.score += completed_columns * 7

        complete_colors = 0
        for color in COLORS:
            positions = [
                (row, WALL_PATTERN[row].index(color))
                for row in range(5)
            ]
            if all(self.wall[row][col] for row, col in positions):
                complete_colors += 1
        self.score += complete_colors * 10


class AzulGame:
    def __init__(self, player_names: list[str]) -> None:
        if not 2 <= len(player_names) <= 4:
            raise ValueError("El juego admite entre 2 y 4 jugadores.")

        self.players = [Player(name) for name in player_names]
        self.bag = [color for color in COLORS for _ in range(20)]
        random.shuffle(self.bag)

        self.discard: list[str] = []
        self.factories: list[list[str]] = []
        self.center: list[str] = []

        self.first_player_token_in_center = True
        self.current_player = 0
        self.next_round_start_player = 0
        self.round_number = 1

    @property
    def factory_count(self) -> int:
        return {2: 5, 3: 7, 4: 9}[len(self.players)]

    def draw_tile(self) -> Optional[str]:
        if not self.bag:
            if not self.discard:
                return None

            self.bag = self.discard
            self.discard = []
            random.shuffle(self.bag)

        return self.bag.pop()

    def setup_round(self) -> None:
        self.factories = []
        self.center = []
        self.first_player_token_in_center = True

        for _ in range(self.factory_count):
            factory: list[str] = []

            for _ in range(4):
                tile = self.draw_tile()
                if tile is not None:
                    factory.append(tile)

            self.factories.append(factory)

    def sources_available(self) -> bool:
        return any(self.factories) or bool(self.center)

    def display_state(self) -> None:
        print("\n" + "=" * 70)
        print(f"RONDA {self.round_number}")
        print("=" * 70)

        for index, factory in enumerate(self.factories, start=1):
            tiles = " ".join(factory) if factory else "-"
            print(f"Fábrica {index}: {tiles}")

        center = " ".join(self.center) if self.center else "-"
        token = (
            " + ficha de primer jugador"
            if self.first_player_token_in_center
            else ""
        )
        print(f"Centro: {center}{token}")

        for player in self.players:
            self.display_player(player)

    def display_player(self, player: Player) -> None:
        print(f"\n{player.name} | Puntos: {player.score}")
        print("Líneas de patrón:")

        for row, line in enumerate(player.pattern_lines):
            capacity = row + 1
            display = ["."] * (capacity - len(line)) + line
            print(f"  {row + 1}: {' '.join(display)}")

        print("Muro:")
        for row in range(5):
            cells = [
                WALL_PATTERN[row][col] if player.wall[row][col] else "."
                for col in range(5)
            ]
            print("   " + " ".join(cells))

        floor = " ".join(player.floor) if player.floor else "-"
        print(f"Suelo: {floor}")

    def choose_source(self) -> tuple[str, int]:
        while True:
            option = input(
                "Elige F<número> para una fábrica o C para el centro: "
            ).strip().upper()

            if option == "C":
                if self.center:
                    return "center", -1
                print("El centro no tiene losetas.")
                continue

            if option.startswith("F") and option[1:].isdigit():
                index = int(option[1:]) - 1

                if 0 <= index < len(self.factories) and self.factories[index]:
                    return "factory", index

            print("Fuente inválida.")

    def choose_color(self, source_tiles: list[str]) -> str:
        valid_colors = sorted(set(source_tiles), key=COLORS.index)

        while True:
            color = input(
                f"Elige color ({', '.join(valid_colors)}): "
            ).strip().upper()

            if color in valid_colors:
                return color

            print("Color inválido.")

    def choose_pattern_line(
        self,
        player: Player,
        color: str,
    ) -> Optional[int]:
        valid_rows = [
            row
            for row in range(5)
            if player.can_place_in_pattern_line(row, color)
        ]

        if not valid_rows:
            print("No hay una línea válida. Las losetas irán al suelo.")
            return None

        valid_display = ", ".join(str(row + 1) for row in valid_rows)

        while True:
            option = input(
                f"Elige línea ({valid_display}) o S para el suelo: "
            ).strip().upper()

            if option == "S":
                return None

            if option.isdigit():
                row = int(option) - 1
                if row in valid_rows:
                    return row

            print("Línea inválida.")

    def take_turn(self) -> None:
        player = self.players[self.current_player]
        print(f"\nTurno de {player.name}")

        source_type, index = self.choose_source()

        if source_type == "center":
            source_tiles = self.center
        else:
            source_tiles = self.factories[index]

        color = self.choose_color(source_tiles)
        selected = [tile for tile in source_tiles if tile == color]
        remaining = [tile for tile in source_tiles if tile != color]

        if source_type == "factory":
            self.factories[index] = []
            self.center.extend(remaining)
        else:
            self.center = remaining

            if self.first_player_token_in_center:
                self.first_player_token_in_center = False
                player.floor.append("1")
                self.next_round_start_player = self.current_player

        row = self.choose_pattern_line(player, color)
        player.place_tiles(row, color, len(selected))

        self.current_player = (
            self.current_player + 1
        ) % len(self.players)

    def finish_round(self) -> None:
        for player in self.players:
            self.discard.extend(player.finish_round())

        self.current_player = self.next_round_start_player

    def play(self) -> None:
        while True:
            self.setup_round()

            while self.sources_available():
                self.display_state()
                self.take_turn()

            self.finish_round()

            if any(player.has_complete_row() for player in self.players):
                break

            self.round_number += 1

        for player in self.players:
            player.add_end_game_bonuses()

        self.display_state()

        ranking = sorted(
            self.players,
            key=lambda player: player.score,
            reverse=True,
        )

        print("\nRESULTADO FINAL")
        print("-" * 30)

        for position, player in enumerate(ranking, start=1):
            print(f"{position}. {player.name}: {player.score} puntos")


def main() -> None:
    print("AZUL - Versión de consola en Python")
    print("B=Azul, Y=Amarillo, R=Rojo, K=Negro, W=Blanco\n")

    while True:
        try:
            player_count = int(input("Número de jugadores (2-4): "))

            if 2 <= player_count <= 4:
                break

        except ValueError:
            pass

        print("Ingresa un número entre 2 y 4.")

    names: list[str] = []

    for index in range(player_count):
        name = input(
            f"Nombre del jugador {index + 1}: "
        ).strip()
        names.append(name or f"Jugador {index + 1}")

    game = AzulGame(names)
    game.play()


if __name__ == "__main__":
    main()
