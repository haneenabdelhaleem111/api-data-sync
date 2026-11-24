import logging
from pydantic import ValidationError
from src.models import GitHubEvent


def validate_events(events):
    valid_events = []
    invalid_events = []

    logging.info("Starting events validation")

    for event in events:
        try:
            validated_event = GitHubEvent.model_validate(event)
            valid_events.append(validated_event)

        except ValidationError as e:
            invalid_events.append(event)
            logging.error(
                f"Invalid event: {event.get('id', 'Unknown ID')} - {e}"
            )

    logging.info(f"Valid events: {len(valid_events)}")
    logging.info(f"Invalid events: {len(invalid_events)}")

    return valid_events, invalid_events
