import sqlite3
import os
from typing import List
from db.core_db.core_db import CoreDB



class TicketDB(CoreDB):

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets_db (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                giveaway_id INTEGER NOT NULL,
                is_freeze BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users_db(user_id) ON DELETE CASCADE,
                FOREIGN KEY (giveaway_id) REFERENCES giveaways_db(giveaway_id) ON DELETE CASCADE
            )
        """)
    
    def delete_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            DROP TABLE IF EXISTS tickets_db
        """)

        conn.commit()
        conn.close()
    
    def add_ticket_to_user(self, user_id: int, giveaway_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tickets_db (user_id, giveaway_id)
            VALUES (?, ?)
        """, (user_id, giveaway_id))

        conn.commit()
        conn.close()
        
    def get_user_tickets(self, user_id: int) -> list[tuple]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM tickets_db
            WHERE user_id = ?
        """, (user_id,))

        tickets = cursor.fetchall()

        conn.close()

        return tickets
    
    def freeze_ticket(self, ticket_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tickets_db
            SET is_freeze = TRUE
            WHERE ticket_id = ?
        """, (ticket_id,))

        conn.commit()
        conn.close()
    
    def unfreeze_ticket(self, ticket_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tickets_db
            SET is_freeze = FALSE
            WHERE ticket_id = ?
        """, (ticket_id,))

        conn.commit()
        conn.close()
        
    