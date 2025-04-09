from core.date.date import Date




class Giveaways:
    def __init__(
            self,
            giveaway_id: int,
            title: str,
            creator_id: int, 
            end_date: Date,
            needed_chanels: dict,
            is_in_catalog: bool = False,
    ):
        self.id = giveaway_id
        self.title = title
        self.creator_id = creator_id
        self.end_date = end_date
        self.needed_channels = needed_chanels
        self.is_in_catalog = is_in_catalog

    