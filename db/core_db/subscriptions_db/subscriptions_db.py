import os
import sqlite3
from core.admin.admin import Subscription as Subscrtiption
from core.date.date import Date
from db.core_db.core_db import CoreDB


class SubscriptionDB(CoreDB):

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions_db (
                subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscription_level INTEGER DEFAULT 0,
                subscription_end_time TEXT,
                admin_id INTEGER,
                FOREIGN KEY (admin_id) REFERENCES admins_db(admin_id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        conn.close()

    def delete_table(self):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS subscriptions_db")
        conn.commit()
        conn.close()

    def add_subscription(self, admin_id: int, subscription: Subscrtiption = Subscrtiption()): 
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Преобразуем объект Date в строку
        end_time_str = str(subscription.subscriptin_end_time)

        cursor.execute(
            "INSERT INTO subscriptions_db (subscription_level, subscription_end_time, admin_id) VALUES (?, ?, ?)",
            (subscription.subscriptin_level, end_time_str, admin_id))

        conn.commit()

        subscription_id = cursor.lastrowid

        conn.close()

        return subscription_id

    def get_subscription_by_id(self, subscription_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Изменен запрос, чтобы возвращать только нужные столбцы
        cursor.execute(
            "SELECT subscription_id, subscription_level, subscription_end_time FROM subscriptions_db WHERE subscription_id = ?",
            (subscription_id,))

        subscription_data = cursor.fetchone()
        conn.close()

        subscription_id, subscription_level, subscription_end_time_str = subscription_data
        
        day, month = map(int, subscription_end_time_str.split('.'))
        subscription_end_time = Date(day=day, month=month)
        subscription = Subscrtiption(subscription_end_time, subscription_level)
        return subscription
            