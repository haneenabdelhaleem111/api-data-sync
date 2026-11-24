
import sqlite3
import pytest
from unittest.mock import patch
from src.processor import process_pending_events


from src.models import GitHubEvent
from src.storage import (
    save_events,
    get_all_events,
    update_event_status,
    get_pending_events,
)


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_events.db"

    monkeypatch.setattr("src.storage.DB_PATH", db_path)

    with sqlite3.connect(db_path) as connection:
        connection.execute("""
            CREATE TABLE events (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                repo_name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending'
            )
        """)

    return db_path


def test_save_new_events(test_db):
    events = [
        {
            "id": "101",
            "type": "PushEvent",
            "repo": {"name": "user/project"}
        },
        {
            "id": "102",
            "type": "WatchEvent",
            "repo": {"name": "user/another-project"}
        }
    ]

    validated_events = [
        GitHubEvent.model_validate(event)
        for event in events
    ]

    new_count, duplicate_count = save_events(validated_events)

    assert new_count == 2
    assert duplicate_count == 0


def test_prevent_duplicate_events(test_db):
    event = GitHubEvent.model_validate({
        "id": "101",
        "type": "PushEvent",
        "repo": {"name": "user/project"}
    })

    save_events([event])

    new_count, duplicate_count = save_events([event])

    assert new_count == 0
    assert duplicate_count == 1


def test_get_all_events(test_db):
    event = GitHubEvent.model_validate({
        "id": "201",
        "type": "PushEvent",
        "repo": {"name": "user/project"}
    })

    save_events([event])

    events = get_all_events()

    assert len(events) == 1
    assert events[0][0] == "201"
    assert events[0][1] == "PushEvent"
    assert events[0][2] == "user/project"


def test_update_event_status(test_db):
    event = GitHubEvent.model_validate({
        "id": "101",
        "type": "PushEvent",
        "repo": {"name": "user/project"}
    })

    save_events([event])

    updated = update_event_status("101", "Completed")

    assert updated == 1

    with sqlite3.connect(test_db) as connection:
        cursor = connection.execute(
            "SELECT status FROM events WHERE id = ?",
            ("101",)
        )

        status = cursor.fetchone()[0]

    assert status == "Completed"


def test_update_invalid_status(test_db):
    event = GitHubEvent.model_validate({
        "id": "101",
        "type": "PushEvent",
        "repo": {"name": "user/project"}
    })

    save_events([event])

    with pytest.raises(ValueError):
        update_event_status("101", "Done")

def test_update_non_existing_event(test_db):
    updated = update_event_status("999", "Completed")

    assert updated == 0


def test_get_pending_events(test_db):
    events = [
        GitHubEvent.model_validate({
            "id": "101",
            "type": "PushEvent",
            "repo": {"name": "user/project1"}
        }),
        GitHubEvent.model_validate({
            "id": "102",
            "type": "WatchEvent",
            "repo": {"name": "user/project2"}
        })
    ]

    save_events(events)

    update_event_status("101", "Completed")

    pending_events = get_pending_events()

    assert len(pending_events) == 1
    assert pending_events[0][0] == "102"



def test_save_events_is_idempotent(test_db):
    event = GitHubEvent(
        id="repeat-101",
        type="PushEvent",
        repo={"name": "user/project"}
    )

    # First synchronization
    new_count, duplicate_count = save_events([event])

    assert new_count == 1
    assert duplicate_count == 0

    # Second synchronization with the same event
    new_count, duplicate_count = save_events([event])

    assert new_count == 0
    assert duplicate_count == 1

    # Verify that only one record exists
    events = get_all_events()

    assert len(events) == 1



def test_completed_events_are_not_processed_again(test_db):

    event = GitHubEvent(
        id="completed-101",
        type="PushEvent",
        repo={"name": "user/project"}
    )

    # Step 1: Save event
    save_events([event])

    # Step 2: Mark event as Completed
    update_event_status("completed-101", "Completed")

    # Step 3: Run pending event processor
    with patch("src.processor.process_event") as mock_process:

        completed, failed = process_pending_events()

        # Step 4: Verify no event was processed again
        mock_process.assert_not_called()

    assert completed == 0
    assert failed == 0

    # Step 5: Verify there are no pending events
    assert get_pending_events() == []
