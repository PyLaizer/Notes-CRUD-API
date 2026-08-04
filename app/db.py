import sqlite3
from contextlib import contextmanager
from typing import Generator

DB_FILE = "notes_database.db"

# Database Initializer
def init_db():
    """Creates the notes table on application startup."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# Connection dependency
# @contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager to yield a database connection.
    Ensures the connection closes properly even if exceptions occur.
    """
    conn = sqlite3.connect(DB_FILE)
    # Enable row factory to access columns by name (like dictionaries)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
