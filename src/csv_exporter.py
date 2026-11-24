
import csv
from pathlib import Path
from src.storage import get_all_events

BASE_DIR = Path(__file__).resolve().parent.parent

def export_events_to_csv():
    events = get_all_events()

    export_dir = BASE_DIR / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    csv_path = export_dir / "events.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["id", "event_type", "repo_name"])
        writer.writerows(events)

    return csv_path, len(events)
