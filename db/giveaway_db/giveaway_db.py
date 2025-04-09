# core/db/giveaway_db/giveaway_db.py
import sqlite3
import os
from typing import List, Optional
from core.date.date import Date



class GiveawayDB:
    """Class for interacting with the giveaway contests database."""
    
    def __init__(self, db_name: str = "giveaway.db"):
        self.db_name = os.path.join(os.path.dirname(__file__), db_name)  # Store the database in the same directory as the script
        # self.create_contests_table()

    def create_contests_table(self):
        """Creates the contests table if it doesn't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contests (
                giveaway_id INTEGER PRIMARY KEY AUTOINCREMENT,
                giveaway_title TEXT NOT NULL,
                creator_id INTEGER NOT NULL,
                is_in_catalog BOOLEAN DEFAULT FALSE,
                needed_channels TEXT,
                end_date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def delete_contests_table(self):
        """Deletes the contests table if it exists."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS contests")
        conn.commit()
        conn.close()

    def add_contest(self, giveaway_title: str, creator_id: int, needed_channels: List[str], is_in_catalog: bool = False, end_date: Date = None):
        """Adds a new contest to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        needed_channels_str = ",".join(needed_channels) if needed_channels else ""  # Преобразуем список в строку
        cursor.execute(
            "INSERT INTO contests (giveaway_title, creator_id, is_in_catalog, needed_channels, end_date) VALUES (?, ?, ?, ?, ?)",
            (giveaway_title, creator_id, is_in_catalog, needed_channels_str, end_date)  # Изменен порядок параметров
        )
        conn.commit()
        conn.close()

    def get_all_contests(self) -> List[tuple]:
        """Retrieves all contests from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contests")
        contests = cursor.fetchall()
        conn.close()
        return contests

    def get_contest_by_id(self, contest_id: int) -> Optional[tuple]:
        """Retrieves a contest by its ID."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contests WHERE giveaway_id = ?", (contest_id,))
        contest = cursor.fetchone()
        conn.close()
        return contest

    def delete_contest(self, contest_id: int):
        """Deletes a contest by its ID."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contests WHERE giveaway_id = ?", (contest_id,))
        conn.commit()
        conn.close()

    def get_channels_for_contest(self, contest_id: int) -> List[str] | None:
        """Retrieves the list of channels for a specific contest."""
        contest = self.get_contest_by_id(contest_id)
        if contest:
            channels_str = contest[4]  # Assuming channels are in the 5th column (index 4)
            return channels_str.split(",") if channels_str else []
        return None

if __name__ == "__main__":
    db = GiveawayDB()

    inp = input("Введите команду:")
    while inp != "exit":
        if inp == "create_table":
            db.create_contests_table()
        elif inp == "delete_table":
            db.delete_contests_table()
        inp = input("Введите команду:")
        