import sqlite3
from datetime import datetime

DB_PATH = "data/youtube.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_channels_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL
            )
        """)


def create_videos_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS videos(
            yt_videoid TEXT PRIMARY KEY NOT NULL,
            title TEXT NOT NULL,
            link TEXT,
            name TEXT NOT NULL,
            published TEXT,
            thumbnail TEXT,
            channel_id TEXT NOT NULL,

            FOREIGN KEY (channel_id)
                REFERENCES channels(channel_id)
            ON DELETE CASCADE
            )
            """)



def save_channel_to_database(channel_id, name):
        try:
            with get_connection() as connection:
                connection.execute("""
                    INSERT INTO channels (channel_id, name)
                    VALUES (?, ?)
                """, (channel_id, name))

            return True

        except sqlite3.IntegrityError:
            print("Channel already exists in database")

            return False

def return_list_of_channels_in_db():
    channels = []

    with get_connection() as connection:
        rows = connection.execute(
            "SELECT channel_id, name FROM channels"
        ).fetchall()

        for row in rows:
            channels.append({
                "channel_id": row["channel_id"],
                "name": row["name"]
            })

    return channels

def add_video_to_database(yt_videoid, title, link, name, published, thumbnail, channel_id):
    with get_connection() as connection:
        connection.execute("""
            INSERT OR IGNORE INTO videos (
            yt_videoid,
            title,
            link,
            name,
            published,
            thumbnail,
            channel_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (yt_videoid, title, link, name, published, thumbnail, channel_id))



def check_if_video_exist_in_database(published, channel_id):
    with get_connection() as connection:
        newest_in_database_from_given_channel = connection.execute("""
            SELECT MAX(published)
            FROM videos
            WHERE channel_id = ?
            """,(channel_id,)).fetchone()[0]

    if newest_in_database_from_given_channel is None:
        return False

    published = datetime.fromisoformat(published)
    newest_in_database_from_given_channel = datetime.fromisoformat(newest_in_database_from_given_channel)

    return published <= newest_in_database_from_given_channel



def delete_channel(channel_id):
    with get_connection() as connection:
        connection.execute("""
            DELETE FROM CHANNELS WHERE channel_id = ?
            """,(channel_id,))

def get_channel_list():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM channels
            """).fetchall()

        return rows
