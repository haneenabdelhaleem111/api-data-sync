
def print_report(
    total_count,
    valid_count,
    invalid_count,
    new_count,
    duplicate_count,
    completed_count,
    failed_count,
    pending_count
):
    print("\n========== Synchronization Report ==========")

    print(f"Total Events: {total_count}")
    print(f"Valid Events: {valid_count}")
    print(f"Invalid Events: {invalid_count}")
    print(f"New Events: {new_count}")
    print(f"Duplicate Events: {duplicate_count}")

    print("\n========== Processing Report ==========")

    print(f"Completed Events: {completed_count}")
    print(f"Failed Events: {failed_count}")
    print(f"Pending Events: {pending_count}")

    print("\n==========================================")
