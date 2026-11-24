import sqlite3
import pytest


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_events.db"

    monkeypatch.setattr("src.storage.DB_PATH", db_path)

    with sqlite3.connect(db_path) as connection:
       connection.execute("""
    CREATE TABLE events (
        id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        repo_name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending'
    )
""")

    return db_path
