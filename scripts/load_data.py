import os
import pandas as pd
import sqlite3
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
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(BASE_DIR, "jobs.db")


# -------------------------------
# Load processed data
# -------------------------------
def load_processed_data():
    file_path = os.path.join(PROCESSED_DIR, "clean_jobs.csv")

    if not os.path.exists(file_path):
        raise Exception("Processed file not found")

    logging.info(f"Loading processed data from {file_path}")
    return pd.read_csv(file_path)


# -------------------------------
# Create database + table
# -------------------------------
def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        salary_min REAL,
        salary_max REAL,
        skills TEXT
    );
    """
    conn.execute(query)
    conn.commit()


# -------------------------------
# Insert data into DB
# -------------------------------
def insert_data(conn, df):
    # Drop columns not in DB
    df = df.drop(columns=["description"], errors="ignore")

# Remove duplicates
    df = df.drop_duplicates(subset=["title", "company", "location"])

    df.to_sql("jobs", conn, if_exists="append", index=False)

    logging.info(f"Inserted {len(df)} records into database")


# -------------------------------
# Main function
# -------------------------------
def main():
    logging.info("Starting data loading process...")

    df = load_processed_data()

    conn = sqlite3.connect(DB_PATH)

    create_table(conn)
    insert_data(conn, df)

    conn.close()

    logging.info("Data successfully loaded into database.")


if __name__ == "__main__":
    main()
