
from pathlib import Path

import src.main as main_module


def test_main_pipeline(monkeypatch):

    calls = []
    report_data = {}

    fake_events = [
        {"id": "101"},
        {"id": "102"}
    ]

    fake_valid_events = [
        {"id": "101"}
    ]

    fake_invalid_events = [
        {"id": "102"}
    ]

    # Mock database initialization
    def fake_initialize_database():
        calls.append("initialize")

    # Mock API request
    def fake_fetch_events():
        calls.append("fetch")
        return fake_events

    # Mock validation
    def fake_validate_events(events):
        calls.append("validate")
        assert events == fake_events

        return fake_valid_events, fake_invalid_events

    # Mock saving events
    def fake_save_events(events):
        calls.append("save")
        assert events == fake_valid_events

        return 1, 0

    # Mock processing
    def fake_process_pending_events():
        calls.append("process")
        return 1, 0

    # Mock pending events
    def fake_get_pending_events():
        calls.append("get_pending")
        return []

    # Capture final report
    def fake_print_report(**kwargs):
        calls.append("report")
        report_data.update(kwargs)

    # Mock CSV export
    def fake_export_events_to_csv():
        calls.append("export")
        return Path("exports/events.csv"), 1

    monkeypatch.setattr(
        main_module,
        "initialize_database",
        fake_initialize_database
    )

    monkeypatch.setattr(
        main_module,
        "fetch_events",
        fake_fetch_events
    )

    monkeypatch.setattr(
        main_module,
        "validate_events",
        fake_validate_events
    )

    monkeypatch.setattr(
        main_module,
        "save_events",
        fake_save_events
    )

    monkeypatch.setattr(
        main_module,
        "process_pending_events",
        fake_process_pending_events
    )

    monkeypatch.setattr(
        main_module,
        "get_pending_events",
        fake_get_pending_events
    )

    monkeypatch.setattr(
        main_module,
        "print_report",
        fake_print_report
    )

    monkeypatch.setattr(
        main_module,
        "export_events_to_csv",
        fake_export_events_to_csv
    )

    # Run the complete pipeline
    main_module.main()

    # Verify execution order
    assert calls == [
        "initialize",
        "fetch",
        "validate",
        "save",
        "process",
        "get_pending",
        "report",
        "export"
    ]

    # Verify final report values
    assert report_data["total_count"] == 2
    assert report_data["valid_count"] == 1
    assert report_data["invalid_count"] == 1
    assert report_data["new_count"] == 1
    assert report_data["duplicate_count"] == 0
    assert report_data["completed_count"] == 1
    assert report_data["failed_count"] == 0
    assert report_data["pending_count"] == 0
