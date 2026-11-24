import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "events.db"

def migrate_database():
    with sqlite3.connect(DB_PATH) as connection:

        cursor = connection.execute(
            "PRAGMA table_info(events)"
        )

        columns = [row[1] for row in cursor.fetchall()]

        if "status" not in columns:
            connection.execute("""
                ALTER TABLE events
                ADD COLUMN status TEXT NOT NULL DEFAULT 'Pending'
            """)

            print("Database migration completed: status column added")

        else:
            print("Database is already up to date")

def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                repo_name TEXT NOT NULL
            )
        """)

    migrate_database()

    print("Database initialized successfully")



def save_events(events):
    new_count = 0
    duplicate_count = 0

    with sqlite3.connect(DB_PATH) as connection:

        for event in events:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO events
                (id, event_type, repo_name)
                VALUES (?, ?, ?)
                """,
                # Use parameterized queries to safely insert event data. parameterized query is the quesion marks above
                (
                    str(event.id),
                    event.type,
                    event.repo.name
                )
            )

# rowcount is 1 for a new record and 0 for an ignored duplicate.
            if cursor.rowcount == 1:
                new_count += 1
            else:
                duplicate_count += 1

    return new_count, duplicate_count

def update_event_status(event_id, status):

    allowed_statuses = ["Pending", "Completed"]

    if status not in allowed_statuses:
        raise ValueError(f"Invalid status: {status}")

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            UPDATE events
            SET status = ?
            WHERE id = ?
            """,
            (status, str(event_id))
        )

        return cursor.rowcount

def get_all_events():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute("""
            SELECT id, event_type, repo_name
            FROM events
        """)

        return cursor.fetchall()


def get_pending_events():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute("""
            SELECT id, event_type, repo_name
            FROM events
            WHERE status = 'Pending'
        """)

        return cursor.fetchall()


def check_database():
    with sqlite3.connect(DB_PATH) as connection:

        cursor = connection.execute("PRAGMA table_info(events)")
        columns = cursor.fetchall()

        print("\n--- Database Columns ---")
        for column in columns:
            print(column[1])

        cursor = connection.execute("""
            SELECT id, status
            FROM events
            LIMIT 5
        """)

        print("\n--- Existing Events Status ---")
        for row in cursor.fetchall():
            print(row)

if __name__ == "__main__":
    initialize_database()

    # Get all pending events
    pending_events = get_pending_events()

    # Display pending events count
    print(f"\nTotal Pending Events: {len(pending_events)}")

    # Display first 10 pending events
    for event in pending_events[:10]:
        print(event)