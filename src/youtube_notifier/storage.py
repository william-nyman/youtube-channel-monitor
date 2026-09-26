import sqlite3

DB_PATH = "data/youtube.db"

def save_channel_to_database(channel_id, name):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            name TEXT
            )
        """)
        try:
            connection.execute("""
                INSERT INTO channels (channel_id, name)
                VALUES (?, ?)
            """, (channel_id, name))
        except sqlite3.IntegrityError:
            print("Channel already exists in database")

def return_list_of_channels_in_db():
    channels = []

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            "SELECT channel_id, name FROM channels"
        ).fetchall()

        for row in rows:
            channels.append({
                "channel_id": row["channel_id"],
                "name": row["name"]
            })

    return channels
