from datetime import datetime


class VideoRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_videos_table(self):
        self.connection.execute("""
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

    def add_video_to_database(
        self, yt_videoid, title, link, name, published, thumbnail, channel_id
    ):

        self.connection.execute(
            """
            INSERT INTO videos (
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

    def check_if_video_exist_in_database(self, published, channel_id, yt_videoid):
        newest = self.connection.execute(
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

        matching_video = self.connection.execute(
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
