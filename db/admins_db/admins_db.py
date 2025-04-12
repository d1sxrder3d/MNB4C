# db/admins_db/admins_db.py
import sqlite3
import os
from typing import List, Optional
from core.date.date import Date
from core.admin.admin import Subscription


class AdminDB:
    def __init__(self, db_name: str = "data.db"):
        self.db_name = os.path.join(os.path.dirname("db/admins_db"), db_name)

    def create_table(self):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins_db (
                admin_id INTEGER NOT NULL,
                admin_name TEXT,
                subscrption_id INTEGER,
                FOREIGN KEY (subscrption_id) REFERENCES subscriptions_db(subscrption_id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        conn.close()

    def delete_table(self):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS admins_db")

        conn.commit()
        conn.close()

    def add_admin(self, user_id, user_name, subscription, giveaways):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO admins_db (admin_id, admin_name, subscrption, giveaways) VALUES (?, ?, ?, ?)",
            (user_id, user_name, str(subscription), ",".join(map(str, giveaways)))
        )

        conn.commit()
        conn.close()

    def get_admin_by_id(self, admin_id: int) -> Optional[tuple]:
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admins_db WHERE admin_id = ?", (admin_id,))

        admin_data = cursor.fetchone()
        conn.close()
        if admin_data:
            admin_id, admin_name, subscription_str, giveaway_ids_str = admin_data
            subscription = Subscription.from_string(subscription_str)
            giveaway_ids = [int(id) for id in giveaway_ids_str.split(',') if giveaway_ids_str] if giveaway_ids_str else []
            return admin_id, admin_name, subscription, giveaway_ids
        return None

    def get_all_admins(self) -> List[tuple]:
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins_db")
        admins_data = cursor.fetchall()
        conn.close()
        admins = []
        for admin_data in admins_data:
            admin_id, admin_name, subscription_str, giveaway_ids_str = admin_data
            subscription = Subscription.from_string(subscription_str)
            giveaway_ids = [int(id) for id in giveaway_ids_str.split(',') if giveaway_ids_str] if giveaway_ids_str else []
            admins.append((admin_id, admin_name, subscription, giveaway_ids))
        return admins

    def update_admin(self, user_id, user_name, subscription, giveaways):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE admins_db SET admin_name = ?, subscrption = ?, giveaways = ? WHERE admin_id = ?",
            (user_name, str(subscription), ",".join(map(str, giveaways)), user_id)
        )

        conn.commit()
        conn.close()

    
