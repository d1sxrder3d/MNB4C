import sqlite3
import os
import array


class TicketDB:
    def __init__(self, db_name: str = "data.db"):
        self.db_name = os.path.join(os.path.dirname("db/tickets_db"), db_name)

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets_db (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                giveaway_id INTEGER NOT NULL,
                is_freeze BOOLEAN DEFAULT FALSE
                
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
        
    def get_user_tickets(self, user_id: int) -> array:
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
        
    