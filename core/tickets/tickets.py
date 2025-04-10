

class Tickets:
    def __init__(self, user_id: int, giveaway_id: int, is_freeze: bool = False):
        self.ticket_id: int
        self.user_id = user_id
        self.giveaway_id = giveaway_id
        self.is_freeze = is_freeze
    
    def freeze(self):
        self.is_freeze = True
    
    def unfreeze(self):
        self.is_freeze = False