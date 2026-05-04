import os
import json
import pandas as pd
import logging

# -------------------------------
# Setup logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# Define paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

# -------------------------------
# Load latest raw file
# -------------------------------
def load_latest_file():
    files = [f for f in os.listdir(RAW_DIR) if f.endswith(".json")]
    if not files:
        raise Exception("No raw data files found")

    latest_file = sorted(files)[-1]
    filepath = os.path.join(RAW_DIR, latest_file)

    logging.info(f"Loading file: {filepath}")

    with open(filepath, "r") as f:
        data = json.load(f)

    return data


# -------------------------------
# Extract relevant fields
# -------------------------------
def extract_jobs(data):
    jobs = data.get("results", [])

    records = []

    for job in jobs:
        record = {
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "description": job.get("description")
        }
        records.append(record)

    return pd.DataFrame(records)


# -------------------------------
# Extract skills (basic NLP)
# -------------------------------
def extract_skills(df):
    skills = ["python", "sql", "aws", "azure", "java", "pandas"]

    def find_skills(text):
        if not isinstance(text, str):
            return []

        text = text.lower()
        found = [skill for skill in skills if skill in text]
        return ", ".join(found)

    df["skills"] = df["description"].apply(find_skills)
    return df


# -------------------------------
# Clean data
# -------------------------------
def clean_data(df):
    df = df.dropna(subset=["title", "company"])
    df = df.fillna("Not specified")
    return df


# -------------------------------
# Save processed data
# -------------------------------
def save_processed_data(df):
    output_path = os.path.join(PROCESSED_DIR, "clean_jobs.csv")
    df.to_csv(output_path, index=False)

    logging.info(f"Processed data saved to {output_path}")


# -------------------------------
# Main function
# -------------------------------
def main():
    logging.info("Starting data processing...")

    data = load_latest_file()
    df = extract_jobs(data)
    df = clean_data(df)
    df = extract_skills(df)

    save_processed_data(df)

    logging.info("Data processing completed successfully.")


if __name__ == "__main__":
    main()
