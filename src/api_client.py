import requests
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

URL = "https://api.github.com/events"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError
    )),
    before_sleep=lambda retry_state: logging.warning(
        f"Request failed. Retrying attempt "
        f"{retry_state.attempt_number}..."
    ),
    #وده بيخلي Tenacity يعيد رفع آخر Exception أصلي بدل RetryError.
    reraise=True
)
def fetch_events():
    logging.info("Sending GET request to API")

    try:
        response = requests.get(
            URL,
            timeout=(10, 30)
        )

        response.raise_for_status()

        logging.info(f"Status: {response.status_code}")
        logging.info("Received successful response")

        events = response.json()

        logging.info(f"Total events: {len(events)}")

        return events

    except requests.RequestException:
        logging.warning("API request failed")
        raise
