
import logging
from pathlib import Path

from src.api_client import fetch_events
from src.validator import validate_events
from src.storage import (
    initialize_database,
    save_events,
    get_pending_events
)
from src.reporter import print_report
from src.csv_exporter import export_events_to_csv
from src.processor import process_pending_events


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def main():
    try:
        # Step 1: Initialize database
        initialize_database()

        # Step 2: Fetch events from API
        events = fetch_events()

        # Step 3: Validate events
        valid_events, invalid_events = validate_events(events)

        # Step 4: Save valid events
        new_count, duplicate_count = save_events(valid_events)

        # Step 5: Process pending events
        completed_count, failed_count = process_pending_events()

        # Step 6: Count remaining pending events
        pending_count = len(get_pending_events())

        # Step 7: Print final report
        print_report(
            total_count=len(events),
            valid_count=len(valid_events),
            invalid_count=len(invalid_events),
            new_count=new_count,
            duplicate_count=duplicate_count,
            completed_count=completed_count,
            failed_count=failed_count,
            pending_count=pending_count
        )

        # Step 8: Export data to CSV
        csv_path, exported_count = export_events_to_csv()

        print(f"\nCSV Exported: {exported_count} events")
        print(f"CSV File: {csv_path}")

        logging.info("Synchronization completed successfully")

    except Exception:
        logging.exception("Application failed")
        print("Something went wrong. Check app.log")


if __name__ == "__main__":
    main()
