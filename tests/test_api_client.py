## using mock to simulate the database and test the CSV export functionality
## ther are two ways:
# Python -> github -> Response ::::::: Real API
# Python -> Mock -> Fake Response :::::::::: Mock API


from unittest.mock import patch, Mock

import pytest
import requests

from src.api_client import fetch_events


@patch("src.api_client.requests.get")
def test_fetch_events_success(mock_get):

    fake_events = [
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

    mock_response = Mock()

    mock_response.json.return_value = fake_events

    mock_get.return_value = mock_response

    result = fetch_events()

    mock_get.assert_called_once()

    mock_response.raise_for_status.assert_called_once()

    assert result == fake_events
    assert len(result) == 2



@patch("src.api_client.requests.get")
def test_fetch_events_http_error(mock_get):

    mock_response = Mock()

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("500 Server Error")
    )

    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_events()



@patch("src.api_client.requests.get")
def test_fetch_events_timeout(mock_get):
## forcing the mock to raise a timeout exception when the fetch_events function is called

    mock_get.side_effect = requests.exceptions.Timeout(
        "Request timed out"
    )

    with pytest.raises(requests.exceptions.Timeout):
        fetch_events()


@patch("src.api_client.requests.get")
def test_fetch_events_connection_error(mock_get):

    mock_get.side_effect = requests.exceptions.ConnectionError(
        "Failed to connect to server"
    )

    with pytest.raises(requests.exceptions.ConnectionError):
        fetch_events()

@patch("src.api_client.requests.get")
def test_fetch_events_retry_success(mock_get):
    fake_events = [
        {
            "id": "101",
            "type": "PushEvent",
            "repo": {"name": "user/project"}
        }
    ]

    mock_response = Mock()
    mock_response.json.return_value = fake_events

    # First attempt: Timeout
    # Second attempt: ConnectionError
    # Third attempt: Success
    mock_get.side_effect = [
        requests.exceptions.Timeout("Request timed out"),
        requests.exceptions.ConnectionError("Connection failed"),
        mock_response
    ]

    result = fetch_events()

    assert result == fake_events
    assert mock_get.call_count == 3
