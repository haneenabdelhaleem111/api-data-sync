
import csv

from src.csv_exporter import export_events_to_csv
from src.models import GitHubEvent
from src.storage import save_events


def test_export_events_to_csv(test_db, monkeypatch, tmp_path):
    event = GitHubEvent.model_validate({
        "id": "301",
        "type": "PushEvent",
        "repo": {"name": "user/project"}
    })

    save_events([event])

    monkeypatch.setattr(
        "src.csv_exporter.BASE_DIR",
        tmp_path
    )

    csv_path, exported_count = export_events_to_csv()

    assert csv_path.exists()
    assert exported_count == 1

    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert reader.fieldnames == ["id", "event_type", "repo_name"]
    assert len(rows) == 1
    assert rows[0]["id"] == "301"
    assert rows[0]["event_type"] == "PushEvent"
    assert rows[0]["repo_name"] == "user/project"
