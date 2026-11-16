import sqlite3
from contextlib import closing
from datetime import datetime

DB_PATH = "data/youtube.db"


class ChannelNotFoundInDatabaseError(Exception):
    pass


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_channels_table():
    with closing(get_connection()) as connection, connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            monitor_shorts INTEGER NOT NULL DEFAULT 0 CHECK (monitor_shorts IN (0,1)),
            added_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
            )
        """)


def create_videos_table():
    with closing(get_connection()) as connection, connection:
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
        with closing(get_connection()) as connection, connection:
            connection.execute(
                """
                    INSERT INTO channels (channel_id, name)
                    VALUES (?, ?)
                """,
                (channel_id, name),
            )

        return True

    except sqlite3.IntegrityError:
        print("Channel already exists in database")

        return False


def get_channels():
    channels = []

    with closing(get_connection()) as connection:
        rows = connection.execute(
            "SELECT channel_id, name, monitor_shorts FROM channels"
        ).fetchall()

        for row in rows:
            channels.append(
                {
                    "channel_id": row["channel_id"],
                    "name": row["name"],
                    "monitor_shorts": row["monitor_shorts"],
                }
            )

    return channels


def add_video_to_database(
    yt_videoid, title, link, name, published, thumbnail, channel_id
):
    with closing(get_connection()) as connection, connection:
        connection.execute(
            """
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
            """,
            (yt_videoid, title, link, name, published, thumbnail, channel_id),
        )


def check_if_video_exist_in_database(published, channel_id, yt_videoid):
    with closing(get_connection()) as connection:
        newest = connection.execute(
            """
            SELECT MAX(published)
            FROM videos
            WHERE channel_id = ?
            """,
            (channel_id,),
        ).fetchone()[0]

        if newest is None:
            return False

        published = datetime.fromisoformat(published)
        newest = datetime.fromisoformat(newest)

        matching_video = connection.execute(
            """
            SELECT yt_videoid
            FROM videos
            WHERE channel_id = ? AND yt_videoid = ?
            """,
            (channel_id, yt_videoid),
        ).fetchone()

        if matching_video is None:
            return published <= newest
        else:
            return True


def delete_channel(channel_id):
    with closing(get_connection()) as connection, connection:
        cursor = connection.execute(
            "DELETE FROM channels WHERE channel_id = ?", (channel_id,)
        )

        if cursor.rowcount == 0:
            raise ChannelNotFoundInDatabaseError


def should_monitor_shorts(channel_id):
    with closing(get_connection()) as connection:
        row = connection.execute(
            """
            SELECT monitor_shorts
            FROM channels
            WHERE channel_id = ?
            """,
            (channel_id,),
        ).fetchone()

    if row is None:
        raise ChannelNotFoundInDatabaseError

    return bool(row[0])


def set_monitor_shorts(channel_id, monitor_shorts):
    with closing(get_connection()) as connection, connection:
        cursor = connection.execute(
            """
            UPDATE channels
            set monitor_shorts = ?
            WHERE channel_id = ?
            """,
            (monitor_shorts, channel_id),
        )

        if cursor.rowcount == 0:
            raise ChannelNotFoundInDatabaseError
