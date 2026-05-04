# UK Tech Jobs Data Pipeline

## Overview

This project is an end-to-end data engineering pipeline that collects, processes, and stores UK tech job data from an external API.

The pipeline automates the workflow from data ingestion to storage in a structured database, demonstrating core data engineering concepts such as ETL (Extract, Transform, Load), data cleaning, and pipeline orchestration.

---

## Architecture

API → Raw JSON → Processed CSV → SQLite Database → Automated Pipeline

---

## Tech Stack

* Python
* pandas
* SQLite
* Requests
* Logging
* python-dotenv

---

## Pipeline Components

### 1. Data Ingestion (`ingest_data.py`)

* Fetches job data from Adzuna API
* Stores raw data as timestamped JSON files
* Includes logging and error handling

### 2. Data Processing (`process_data.py`)

* Cleans and transforms raw data using pandas
* Extracts relevant fields (title, company, salary, etc.)
* Performs basic skill extraction (Python, SQL, AWS, etc.)
* Outputs cleaned dataset as CSV

### 3. Data Loading (`load_data.py`)

* Loads processed data into a SQLite database
* Implements table schema
* Removes duplicate records before insertion

### 4. Pipeline Orchestration (`pipeline.py`)

* Runs ingestion, processing, and loading sequentially
* Enables full pipeline execution with a single command

---

## How to Run

### 1. Clone the repository

git clone https://github.com/bhollaaryan7/job-data-pipeline.git
cd job-data-pipeline

### 2. Install dependencies

pip install -r requirements.txt

### 3. Add API credentials

Create a `.env` file in the root directory:

ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

### 4. Run the pipeline

python3 scripts/pipeline.py

---

## Output

* Raw data stored in `data/raw/`
* Processed data stored in `data/processed/clean_jobs.csv`
* Structured data stored in `jobs.db`

---

## Key Features

* End-to-end ETL pipeline
* Modular and maintainable code structure
* Logging and error handling
* Automated workflow execution
* Integration with real-world API data

---

## Future Improvements

* Add scheduling using Airflow
* Deploy pipeline to cloud platforms (AWS or GCP)
* Build a dashboard using Streamlit or Power BI
* Improve skill extraction using advanced NLP

---

## Why This Project

This project demonstrates practical data engineering skills including:

* Building data pipelines
* Working with APIs
* Data transformation and cleaning
* Database design and integration

---

## Author

Aryan
MSc Machine Intelligence
