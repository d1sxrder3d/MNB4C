


class User:
    def __init__(
            self, 
            user_id: int, 
            user_name: str, 
            isbloked: bool = False, 
            isbanned: bool = False, 
            isadmin: bool = False
        ):
        
        self.id = user_id
        self.name = user_name

        self.giveaways = set()

        self.sent_messages = []

        self.isbloked = isbloked
        self.isbanned = isbanned
        self.isadmin = isadmin
    
    


