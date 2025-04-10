# core/db/giveaway_db/giveaway_db.py
import sqlite3
import os
from typing import List, Optional
from core.date.date import Date


class GiveawayDB:
    """Class for interacting with the giveaway contests database."""

    def __init__(self, db_name: str = "data.db"):
        self.db_name = os.path.join(os.path.dirname("db/giveaway_db"), db_name)

    def create_table(self):
        """Creates the contests table if it doesn't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS giveaways_db (
                giveaway_id INTEGER PRIMARY KEY AUTOINCREMENT,
                giveaway_title TEXT NOT NULL,
                is_in_catalog BOOLEAN DEFAULT FALSE,
                needed_channels TEXT,
                end_date TEXT,
                tickets_count INTEGER DEFAULT 0,
                winners_count INTEGER DEFAULT 1,
                winners TEXT DEFAULT ""
            )
        """)
        conn.commit()
        conn.close()

    def delete_table(self):
        """Deletes the contests table if it exists."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS giveaways_db")
        conn.commit()
        conn.close()

    def add_contest(self, giveaway_title: str, needed_channels: List[str], is_in_catalog: bool = False,
                    end_date: Date = None):
        """Adds a new contest to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        needed_channels_str = ",".join(needed_channels) if needed_channels else ""
        cursor.execute(
            "INSERT INTO giveaways_db (giveaway_title, is_in_catalog, needed_channels, end_date) VALUES (?, ?, ?, ?)",
            (giveaway_title, is_in_catalog, needed_channels_str, end_date)
        )
        conn.commit()
        conn.close()

    def get_all_contests(self) -> List[tuple]:
        """Retrieves all giveaways_db from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM giveaways_db")
        contests = cursor.fetchall()
        conn.close()
        return contests

    def delete_contest(self, contest_id: int):
        """Deletes a giveaways_db by its ID."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM giveaways_db WHERE giveaway_id = ?", (contest_id,))
        conn.commit()
        conn.close()

    def get_channels_for_contest(self, contest_id: int) -> List[str] | None:
        """Retrieves the list of channels for a specific contest."""
        contest = self.get_contest_by_id(contest_id)
        if contest:
            channels_str = contest[3]  # Assuming channels are in the 4th column (index 3)
            return channels_str.split(",") if channels_str else []
        return None

    def get_contest_by_id(self, contest_id: int) -> Optional[tuple]:
        """Получает конкурс по его ID."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM giveaways_db WHERE giveaway_id = ?", (contest_id,))

        contest = cursor.fetchone()

        conn.close()

        return contest
