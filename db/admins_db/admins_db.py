# db/admins_db/admins_db.py
import sqlite3
import os
from typing import List, Optional
from core.date.date import Date
from core.admin.admin import Subscription
from db.subscriptions_db.subscriptions_db import SubscriptionDB



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
                subscription_id INTEGER,
                FOREIGN KEY (subscription_id) REFERENCES subscriptions_db(subscription_id) ON DELETE CASCADE
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

    def add_admin(self, user_id: int, user_name: str, subscription: Subscription = Subscription(), giveaways: List[int] = []):
        
        subscription_db = SubscriptionDB()

        subscription_id = subscription_db.add_subscription(user_id, subscription) # Изменено здесь
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        

        cursor.execute(
            "INSERT INTO admins_db (admin_id, admin_name, subscription_id) VALUES (?, ?, ?)",
            (user_id, user_name, subscription_id)
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
            admin_id, admin_name, subscription_id = admin_data
            subscription_db = SubscriptionDB()
            subscription = subscription_db.get_subscription_by_id(subscription_id)
            return admin_id, admin_name, subscription
        return None

    def get_all_admins(self) -> List[tuple]:

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins_db")
        admins_data = cursor.fetchall()
        conn.close()
        admins = []
        for admin_data in admins_data:
            admin_id, admin_name, subscription_id = admin_data
            subscription_db = SubscriptionDB()
            subscription = subscription_db.get_subscription_by_id(subscription_id)
            admins.append((admin_id, admin_name, subscription))
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


