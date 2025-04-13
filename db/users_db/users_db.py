import sqlite3
import os
from typing import List, Optional, Union
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
    
    def add_user(self, user_or_id: Union[User, int], user_name: Optional[str] = None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        if isinstance(user_or_id, User):
            # Случай, когда передан объект User
            user = user_or_id
            cursor.execute("""
                INSERT INTO users_db (user_id, user_name)
                VALUES (?, ?)
            """, (user.user_id, user.user_name))
        elif isinstance(user_or_id, int) and user_name is not None:
            # Случай, когда переданы user_id и user_name
            cursor.execute("""
                INSERT INTO users_db (user_id, user_name)
                VALUES (?, ?)
            """, (user_or_id, user_name))
        elif isinstance(user_or_id, int) and user_name is None:
            user_name = "None"

            cursor.execute("""
                INSERT INTO users_db (user_id, user_name)
                VALUES (?, ?)
            """, (user_or_id, user_name))
            
        else:
            raise TypeError("Invalid arguments for add_user")

        conn.commit()
        conn.close()

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
        conn = sqlite3.connect(self.db_name)
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
        
    
                               