import sqlite3


class ChannelNotFoundInDatabaseError(Exception):
    pass


class ChannelRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_channel_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            monitor_shorts INTEGER NOT NULL DEFAULT 0 CHECK (monitor_shorts IN (0,1)),
            added_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
            )
        """)

    def save_channel(self, channel_id, name):
        try:
            self.connection.execute(
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

    def get_channels(self):
        channels = []

        rows = self.connection.execute(
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

    def delete_channel(self, channel_id):
        rows = self.connection.execute(
            "DELETE FROM channels WHERE channel_id = ?", (channel_id,)
        )

        if rows.rowcount == 0:
            raise ChannelNotFoundInDatabaseError

    def should_monitor_shorts(self, channel_id):
        row = self.connection.execute(
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

    def set_monitor_shorts(self, channel_id, monitor_shorts):
        row = self.connection.execute(
            """
            UPDATE channels
            set monitor_shorts = ?
            WHERE channel_id = ?
            """,
            (monitor_shorts, channel_id),
        )

        if row.rowcount == 0:
            raise ChannelNotFoundInDatabaseError
