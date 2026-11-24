from unittest.mock import patch, call

from src.processor import process_pending_events
##patch: replacin te eal funcions wihpractical nes
@patch("src.processor.get_pending_events")
@patch("src.processor.process_event")
@patch("src.processor.update_event_status")

def test_process_pending_events_success(
    mock_update_status,
    mock_process_event,
    mock_get_pending
):
    mock_get_pending.return_value = [
        ("101", "PushEvent", "user/project"),
        ("102", "WatchEvent", "user/project2")
    ]

    mock_process_event.return_value = True

    completed, failed = process_pending_events()

    assert completed == 2
    assert failed == 0

    assert mock_update_status.call_count == 2
    assert mock_update_status.call_args_list[0].args == (
        "101", "Completed"
    )


    # failing the processing
@patch("src.processor.get_pending_events")
@patch("src.processor.process_event")
@patch("src.processor.update_event_status")
def test_process_pending_events_failure(
    mock_update_status,
    mock_process_event,
    mock_get_pending
):
    mock_get_pending.return_value = [
        ("103", "PushEvent", "user/project")
    ]

    mock_process_event.return_value = False

    completed, failed = process_pending_events()

    assert completed == 0
    assert failed == 1

    mock_update_status.assert_not_called()
    ## making sre that the system didn't update the status of the failed event


@patch("src.processor.get_pending_events")
@patch("src.processor.process_event")
@patch("src.processor.update_event_status")
def test_processing_continues_after_exception(
    mock_update_status,
    mock_process_event,
    mock_get_pending
):
    mock_get_pending.return_value = [
        ("101", "PushEvent", "user/project1"),
        ("102", "WatchEvent", "user/project2"),
        ("103", "PushEvent", "user/project3")
    ]

    mock_process_event.side_effect = [
        True,
        Exception("Processing failed"),
        True
    ]

    completed, failed = process_pending_events()

    assert completed == 2
    assert failed == 1

    assert mock_update_status.call_count == 2

    mock_update_status.assert_any_call("101", "Completed")
    mock_update_status.assert_any_call("103", "Completed")

@patch("src.processor.get_pending_events")
@patch("src.processor.process_event")
@patch("src.processor.update_event_status")
def test_processing_continues_after_failed_event(
    mock_update_status,
    mock_process_event,
    mock_get_pending
):
    mock_get_pending.return_value = [
        ("101", "PushEvent", "user/project1"),
        ("102", "InvalidEvent", None),
        ("103", "DeleteEvent", "user/project3")
    ]

    mock_process_event.side_effect = [
        True,
        False,
        True
    ]

    completed, failed = process_pending_events()

    assert completed == 2
    assert failed == 1

    assert mock_update_status.call_count == 2

    mock_update_status.assert_any_call("101", "Completed")
    mock_update_status.assert_any_call("103", "Completed")
    assert ("102", "Completed") not in [
    call.args for call in mock_update_status.call_args_list
]


from unittest.mock import patch


def test_processing_continues_after_status_update_failure():

    with patch(
        "src.processor.get_pending_events"
    ) as mock_get_pending, patch(
        "src.processor.process_event"
    ) as mock_process_event, patch(
        "src.processor.update_event_status"
    ) as mock_update_status:

        mock_get_pending.return_value = [
            ("101", "PushEvent", "user/project1"),
            ("102", "WatchEvent", "user/project2")
        ]

        mock_process_event.return_value = True

        mock_update_status.side_effect = [
            Exception("Database write failed"),
            None
        ]

        completed, failed = process_pending_events()

        assert completed == 1
        assert failed == 1

        assert mock_process_event.call_count == 2

        assert mock_update_status.call_count == 2

        mock_update_status.assert_any_call(
            "101", "Completed"
        )

        mock_update_status.assert_any_call(
            "102", "Completed"
        )
