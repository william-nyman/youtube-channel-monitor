import sqlite3
from contextlib import closing, contextmanager

DB_PATH = "data/youtube.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def transaction():
    with closing(get_connection()) as connection, connection:
        yield connection
