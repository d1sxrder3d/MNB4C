import array


class User:
    def __init__(
            self, 
            user_id: int, 
            user_name: str, 
            user_tickets: array = [],
            user_giveaways: array = [],
            sent_messages: array = [],
            isbloked: bool = False, 
            isbanned: bool = False

        ):
        
        self.user_id = user_id
        self.user_name = user_name

        self.tickets = user_tickets
        self.user_giveaways = user_giveaways
        self.sent_messages = sent_messages

        self.isbloked = isbloked
        self.isbanned = isbanned
    
    


