"""
Database layer for the Task API.

Handles the SQLite connection, table creation, and seeding of
example data. This is the only file that should ever contain raw
SQL — endpoints in main.py call into these helper functions instead
of talking to sqlite3 directly.
"""
import sqlite3
from pathlib import Path

# The database file lives next to this script, so it doesn't matter
# what directory you launch the app from.
DB_PATH = Path(__file__).parent / "tasks.db"


def get_connection() -> sqlite3.Connection:
    """
    Open a new connection to the database.

    row_factory = sqlite3.Row lets us access columns by name
    (row["title"]) instead of by index (row[1]), and makes it easy
    to convert a row straight into a dict for JSON responses.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enforce foreign keys / other pragmas here later if the schema grows.
    return conn


def init_db() -> None:
    """
    Create the tasks table if it doesn't exist yet, and seed it with
    three example tasks the very first time the app runs.

    This function is safe to call on every application startup:
    - CREATE TABLE IF NOT EXISTS is a no-op if the table is already there.
    - The seed insert only happens when the table is completely empty,
      so restarting the app never duplicates the example tasks.
    """
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done  BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        conn.commit()

        row_count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if row_count == 0:
            example_tasks = [
                ("Buy milk", False),
                ("Write the assignment README", False),
                ("Learn SQL basics", True),
            ]
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                example_tasks,
            )
            conn.commit()
    finally:
        conn.close()