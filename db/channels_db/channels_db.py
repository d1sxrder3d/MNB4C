import os
import sqlite3


class ChannelDB:
    def __init__(self, db_name: str = "data.db"):
        self.db_name = os.path.join(os.path.dirname("db/channels_db"), db_name)

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS channels_db (
                channel_id INTEGER NOT NULL,
                channel_name TEXT NOT NULL,
                giveaway_id INTEGER,
                is_bot_in_channel BOOLEAN,
                FOREIGN KEY (giveaway_id) REFERENCES giveaways_db(giveaway_id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        conn.close()

    def delete_table(self):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS channels_db")
        conn.commit()
        conn.close()
    