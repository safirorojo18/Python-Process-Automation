# Automated Data Extraction and Reporting Pipeline

## Project Overview

This project automates the extraction, cleaning, validation, storage, and reporting of publicly available product data from a practice e-commerce website.

The workflow uses Selenium and Beautiful Soup to collect product information such as title, category, price, availability, rating, and product URL. The extracted records are cleaned and validated with Python and Pandas, stored in CSV and SQLite formats, and summarized in an automated Excel report.

The project was created to demonstrate how repetitive data collection and reporting tasks can be converted into a reusable and reliable business process.

## Business Problem

Manual data collection is time-consuming, repetitive, and prone to errors. Business users often need structured reports from information that is available only on websites or distributed across several pages.

This project addresses that problem by creating an automated pipeline that:

- Extracts product data from multiple web pages.
- Standardizes and validates the collected information.
- Stores historical results in structured formats.
- Generates summary KPIs and an Excel report.
- Records execution details and errors in a log file.

## Project Objectives

- Automate browser-based data extraction.
- Reduce repetitive manual work.
- Validate data quality before reporting.
- Store processed data in CSV and SQLite.
- Generate an Excel report for business users.
- Track failed records and execution status.
- Build a modular and reusable Python workflow.

## Data Source

The project uses Books to Scrape, a public website designed for web scraping practice.

The dataset includes:

- Product title
- Category
- Price
- Availability
- Rating
- Product URL
- Extraction date

## Workflow

1. Launch the automated browser.
2. Navigate through product and category pages.
3. Extract product information.
4. Save the raw data.
5. Clean and standardize the records.
6. Perform data-quality checks.
7. Store the processed data in CSV and SQLite.
8. Generate an Excel report.
9. Save execution details in a log file.

## Key Performance Indicators

The automated report includes:

- Total products extracted
- Average product price
- Minimum and maximum price
- Products by category
- Products by rating
- Availability percentage
- Average price by category
- Number of failed or incomplete records
- Extraction date and execution status


├── reports/
├── logs/
└── screenshots/
