import sqlite3
from contextlib import contextmanager
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "support.db"


@contextmanager
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open', 'in_progress', 'resolved'))
            )
            """
        )
        columns = connection.execute("PRAGMA table_info(tickets)").fetchall()
        if not any(column["name"] == "assignee" for column in columns):
            connection.execute("ALTER TABLE tickets ADD COLUMN assignee TEXT")
        if not any(column["name"] == "category" for column in columns):
            connection.execute(
                """
                ALTER TABLE tickets ADD COLUMN category TEXT NOT NULL DEFAULT 'other'
                    CHECK (category IN ('payment', 'account', 'technical', 'other'))
                """
            )
