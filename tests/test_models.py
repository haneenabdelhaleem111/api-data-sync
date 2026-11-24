
# from src.validator import validate_events


# test_events = [
#     {
#         "id": "12345",
#         "type": "PushEvent",
#         "repo": {
#             "name": "user/project"
#         }
#     },
#     {
#         "id": "67890",
#         "type": "WatchEvent",
#         "repo": {}
#     }
# ]

# valid_events, invalid_events = validate_events(test_events)

# print(f"Valid: {len(valid_events)}")
# print(f"Invalid: {len(invalid_events)}")

# print("\nValid Events:")
# for event in valid_events:
#     print(event.repo.name)

# print("\nInvalid Events:")
# for event in invalid_events:
#     print(event)

from src.models import GitHubEvent


def test_valid_github_event():
    event = {
        "id": "12345",
        "type": "PushEvent",
        "repo": {
            "name": "user/project"
        }
    }

    result = GitHubEvent.model_validate(event)

    assert result.id == "12345"
    assert result.type == "PushEvent"
    assert result.repo.name == "user/project"
