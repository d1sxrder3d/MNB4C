import sqlite3
import os
from typing import List, Optional





class AdminDB:
    def __init__(self, db_name: str = "admins.db"):
        self.db_name = os.path.join(os.path.dirname(__file__), db_name)  # Store the database in the same directory as the script
        # self.create_contests_table()


    def create_contests_table(self):
        """Creates the contests table if it doesn't exist."""
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INTEGER NOT NULL,
                admin_name TEXT,
                subscrption TEXT,
                giveaways TEXT
            )
        """)

        conn.commit()
        conn.close()
        
    def delete_contests_table(self):
        """Deletes the contests table."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS admins")
        
        conn.commit()
        conn.close()

    def add_admin(self, user_id, user_name, subscription, giveaways):
        """Adds a new contest to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO admins (admin_id, admin_name, subscrption, giveaways) VALUES (?, ?, ?, ?)",
            (user_id, user_name, subscription, giveaways)
        )
        
        conn.commit()
        conn.close()

    def get_admin_by_id(self, admin_id: int) -> Optional[tuple]:
        """Retrieves a contest by its ID."""
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM admins WHERE admin_id = ?", (admin_id,))
        
        admin = cursor.fetchone()
        
        conn.close()
        
        return admin
    
        
                


if __name__ == "__main__":
    db = AdminDB()
    inp = input("Введите команду:")
    while inp != "exit":
        if inp == "create_table":
            db.create_contests_table()
        if inp == "delete_table":
            db.delete_contests_table()
        inp = input("Введите команду:")