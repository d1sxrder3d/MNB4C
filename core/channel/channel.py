



class Chanel:
    def __init__(self, channel_id: int, channel_name: str, giveaway_id: int, is_bot_in_channel: bool):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.giveaway_id = giveaway_id
        self.is_bot_in_channel = is_bot_in_channel #прописать функцию чтобы при добавлении бота он создавал channel 
    
    def __str__(self):
        return f"Chanel(id={self.channel_id}, name={self.channel_name}, giveaway_id={self.giveaway_id}, is_bot_in_channel={self.is_bot_in_channel})"
    
    
