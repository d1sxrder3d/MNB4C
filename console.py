from db.giveaway_db.giveaway_db import GiveawayDB
from db.admins_db.admins_db import AdminDB
from db.tickets_db.tickets_db import TicketDB
from db.users_db.users_db import UserDB


def choose_db():
    command = input("Введите название базы данных: ")
    if command == "giveaway_db":
        return commands(GiveawayDB())
    elif command == "admins_db":
        return commands(AdminDB())
    elif command == "users_db":
        return commands(UserDB())
    elif command == "tickets_db":
        return commands(TicketDB())
    elif command == "exit":
        return False
    else:
        choose_db()
        

def commands(db):
    command = input("Введите команду: ")
    if command == "create_table":
        db.create_table()
        commands(db)
    elif command == "delete_table":
        db.delete_table()
        commands(db)
    elif command == "exit":
        choose_db()
    else:
        commands()


if __name__ == "__main__":
    while choose_db() == True:
        a = 1