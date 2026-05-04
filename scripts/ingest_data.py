import requests
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# -------------------------------
# Setup logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# -------------------------------
# Define base directories
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DIR, exist_ok=True)


# -------------------------------
# Fetch job data from API
# -------------------------------
def fetch_jobs():
    url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 20,
        "what": "data engineer",
        "where": "london",
        "content-type": "application/json"
    }

    logging.info("Sending request to Adzuna API...")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response content: {response.text}")
        raise

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        raise

    logging.info("Data fetched successfully.")
    return response.json()


# -------------------------------
# Save raw data to file
# -------------------------------
def save_raw_data(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(RAW_DIR, f"jobs_{timestamp}.json")

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Data saved to {filename}")

    except IOError as io_err:
        logging.error(f"File write error: {io_err}")
        raise


# -------------------------------
# Main pipeline function
# -------------------------------
def main():
    logging.info("Starting data ingestion pipeline...")

    data = fetch_jobs()
    save_raw_data(data)

    logging.info("Ingestion pipeline completed successfully.")


# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    main()
