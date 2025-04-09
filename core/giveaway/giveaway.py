


class Giveaways:
    def __init__(
            self,
            giveaway_id: int,
            title: str,
            creator_id: int, 
            needed_chanels: dict,
            is_in_catalog: bool = False,
            end_date: str = None,
    ):
        self.id = giveaway_id
        self.title = title
        self.creator_id = creator_id
        self.needed_channels = needed_chanels
        self.is_in_catalog = is_in_catalog
        self.end_date = end_date

    