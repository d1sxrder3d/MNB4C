from db.giveaways_db.giveaways_db import GiveawayDB
from db.admins_db.admins_db import AdminDB
from db.tickets_db.tickets_db import TicketDB
from db.users_db.users_db import UserDB
from db.subscriptions_db.subscriptions_db import SubscriptionDB
from db.channels_db.channels_db import ChannelDB


def choose_db():
    command = input("Введите название базы данных: ")
    if command == "delete_all":
        ChannelDB().delete_table()
        SubscriptionDB().delete_table()
        GiveawayDB().delete_table()
        AdminDB().delete_table()
        UserDB().delete_table()
        TicketDB().delete_table()
        choose_db()

    elif command == "create_all":
        ChannelDB().create_table()
        SubscriptionDB().create_table()
        GiveawayDB().create_table()
        AdminDB().create_table()
        UserDB().create_table()
        TicketDB().create_table()
        choose_db()

    elif command == "channels_db":
        return commands(ChannelDB())
    
    elif command == "subscriptions_db":
        return commands(SubscriptionDB())
    
    elif command == "giveaway_db":
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