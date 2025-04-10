import sqlite3
import os
from typing import List, Optional
from core.users.users import User



class UserDB:
    def __init__(self, db_name: str = "data.db"):
        self.db_name = os.path.join(os.path.dirname("db/users_db"), db_name)

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_db (
                user_id INTEGER,
                user_name TEXT,
                isbloked BOOLEAN DEFAULT FALSE,
                isbanned BOOLEAN DEFAULT FALSE
            )
        """)

        conn.commit()
        conn.close()
    def delete_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            DROP TABLE IF EXISTS users_db
        """)

        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, user_name: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users_db (user_id, user_name)
            VALUES (?, ?)
        """, (user_id, user_name))

        conn.commit()
        conn.close()

    def add_user(self,user: User):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users_db (user_id, user_name)
            VALUES (?, ?)
        """, (user.user_id, user.user_name))


    def block_user(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users_db
            SET isbloked = TRUE
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    def unblock_user(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users_db
            SET isbloked = FALSE
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()
    
    def ban_user(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users_db
            SET isbanned = TRUE
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()
    
    def unban_user(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users_db
            SET isbanned = FASLE
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()
    
    def add_giveaway(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users_db (user_id)
            VALUES (?)
        """, (user_id,))

        conn.commit()
        conn.close()

    def get_user_by_id(self, user_id: int) -> Optional[tuple]:
        conn = sqlite3(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users_db
            WHERE user_id = ?
        """, (user_id,))

        user = cursor.fetchone()

        conn.close()

        return user
    
    def get_all_users(self) -> List[tuple]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users_db
        """)

        users = cursor.fetchall()

        conn.close()

        return users
        
    
                               