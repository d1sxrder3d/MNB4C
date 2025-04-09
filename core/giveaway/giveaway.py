


class Giveaways:
    def __init__(
            self,
            giveaway_id: int,
            title: str,
            creator_id: int, 
            needed_groups: dict,
            is_in_catalog: bool = False,
    ):
        self.id = giveaway_id
        self.title = title
        self.creator_id = creator_id
        self.needed_groups = needed_groups
        self.is_in_catalog = is_in_catalog

    