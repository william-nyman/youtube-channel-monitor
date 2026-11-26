from datetime import datetime


class VideoRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_videos_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS videos(
            yt_videoid TEXT PRIMARY KEY NOT NULL,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            name TEXT NOT NULL,
            published TEXT NOT NULL,
            thumbnail TEXT,
            channel_id TEXT NOT NULL,

            FOREIGN KEY (channel_id)
                REFERENCES channels(channel_id)
            ON DELETE CASCADE
            )
            """)

    def add_video_to_database(self, video):

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
            (
                video.yt_videoid,
                video.title,
                video.link,
                video.name,
                video.published,
                video.thumbnail,
                video.channel_id,
            ),
        )

    def check_if_video_exist_in_database(self, video):
        newest = self.connection.execute(
            """
            SELECT MAX(published)
            FROM videos
            WHERE channel_id = ?
            """,
            (video.channel_id,),
        ).fetchone()[0]

        if newest is None:
            return False

        published = datetime.fromisoformat(video.published)
        newest = datetime.fromisoformat(newest)

        matching_video = self.connection.execute(
            """
            SELECT yt_videoid
            FROM videos
            WHERE channel_id = ? AND yt_videoid = ?
            """,
            (video.channel_id, video.yt_videoid),
        ).fetchone()

        if matching_video is None:
            return published <= newest
        else:
            return True
