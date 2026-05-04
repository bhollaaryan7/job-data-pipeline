import logging
import subprocess

# -------------------------------
# Setup logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_script(script_name):
    try:
        logging.info(f"Running {script_name}...")
        subprocess.run(["python3", f"scripts/{script_name}"], check=True)
        logging.info(f"{script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running {script_name}: {e}")
        raise


def main():
    logging.info("Starting full data pipeline...")

    run_script("ingest_data.py")
    run_script("process_data.py")
    run_script("load_data.py")

    logging.info("Full pipeline executed successfully.")


if __name__ == "__main__":
    main()
