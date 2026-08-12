"""
Database layer for the Task API.

Handles the Postgres connection, table creation, and seeding of
example data. This is the only file that should ever contain raw
SQL for setup — endpoints in main.py run their own queries through
the connection/cursor this file provides.
"""
import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    """
    Open a new connection to the database.

    cursor_factory=RealDictCursor lets us access columns by name
    (row["title"]) instead of by index, matching how main.py already
    reads rows (it was written against sqlite3.Row, which behaves
    the same way).
    """
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


def init_db() -> None:
    """
    Create the tasks table if it doesn't exist yet, and seed it with
    three example tasks the very first time the app runs.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id    SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done  BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        conn.commit()

        cursor.execute("SELECT COUNT(*) AS count FROM tasks")
        row_count = cursor.fetchone()["count"]
        if row_count == 0:
            example_tasks = [
                ("Buy milk", False),
                ("Write the assignment README", False),
                ("Learn SQL basics", True),
            ]
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                example_tasks,
            )
            conn.commit()
    finally:
        conn.close()