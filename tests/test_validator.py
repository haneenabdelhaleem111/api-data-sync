
from src.validator import validate_events


def test_validate_valid_events():
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

    valid_events, invalid_events = validate_events(events)

    assert len(valid_events) == 2
    assert len(invalid_events) == 0


def test_validate_invalid_events():
    events = [
        {
            "id": "101",
            "type": "PushEvent",
            "repo": {"name": "user/project"}
        },
        {
            "id": "102",
            "type": "WatchEvent",
            "repo": {}
        }
    ]

    valid_events, invalid_events = validate_events(events)

    assert len(valid_events) == 1
    assert len(invalid_events) == 1
    assert invalid_events[0]["id"] == "102"
