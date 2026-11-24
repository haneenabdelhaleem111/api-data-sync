
import logging

from src.storage import get_pending_events, update_event_status


def process_event(event):
    event_id, event_type, repo_name = event

    logging.info(
        f"Processing event {event_id} "
        f"| Type: {event_type} "
        f"| Repository: {repo_name}"
    )

    try:
        # Step 1: Validate repository name
        if not repo_name:
            raise ValueError("Repository name is missing")

        # Step 2: Process supported event types
        if event_type == "PushEvent":
            print(f"New push detected in {repo_name}")

        elif event_type == "WatchEvent":
            print(f"Repository watched: {repo_name}")

        elif event_type == "DeleteEvent":
            print(f"Delete event detected in {repo_name}")

        elif event_type == "CreateEvent":
             print(f"New resource created in {repo_name}")

        else:
            raise ValueError(
                f"Unsupported event type: {event_type}"
            )

        logging.info(
            f"Event {event_id} processed successfully"
        )

        return True

    except Exception:
        logging.exception(
            f"Failed to process event {event_id}"
        )
        return False


def process_pending_events():
    pending_events = get_pending_events()

    completed_count = 0
    failed_count = 0

    for event in pending_events:
        event_id = event[0]

        try:
            success = process_event(event)

            if success:
                update_event_status(event_id, "Completed")
                completed_count += 1

                logging.info(
                    f"Event {event_id} completed successfully"
                )

            else:
                failed_count += 1

                logging.warning(
                    f"Event {event_id} processing failed. "
                    "Status remains Pending."
                )

        except Exception:
            failed_count += 1

            logging.exception(
                f"Error while processing event {event_id}"
            )

    return completed_count, failed_count


if __name__ == "__main__":
    test_events = [
        ("test-201", "PushEvent", "user/project1"),
    ("test-202", "InvalidEvent", None),
    ("test-203", "DeleteEvent", "user/project3"),
    ("test-204", "CreateEvent", "user/project4"),
    ("test-205", "WatchEvent", "user/project5")
]

    for event in test_events:
        result = process_event(event)
        print(f"Processing Result: {result}")
