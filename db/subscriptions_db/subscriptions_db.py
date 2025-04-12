import os
import sqlite3

class SubscriptionDB:
    def __init__(self, db_name: str = "data.db"):
        self.db_name = os.path.join(os.path.dirname("db/subscriptions_db"), db_name)

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions_db (
                subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscription_level INTEGER DEFAULT 0,
                subscription_end_time TEXT
            )
        """)

        conn.commit()
        conn.close()

    def delete_table(self):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS giveaways_db")
        conn.commit()
        conn.close()
