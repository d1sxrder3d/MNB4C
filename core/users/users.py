


class User:
    def __init__(self, user_id, user_name, isbloked = False, isbanned = False, isadmin = False):
        self.id = user_id
        self.name = user_name

        self.giveaways = set()

        self.sent_messages = []

        self.isbloked = isbloked
        self.isbanned = isbanned
        self.isadmin = isadmin
    
    


