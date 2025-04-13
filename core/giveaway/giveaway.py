from core.date.date import Date


class Giveaways:
    def __init__(
            self,
            giveaway_id: int,
            title: str,
            end_date: Date,
            is_in_catalog: bool = False,
            tickets_count: int = 0,
            winners_count: int = 1,
            winners: str = ""
    ):
        self.giveaway_id = giveaway_id
        self.title = title
        self.end_date = end_date
        self.is_in_catalog = is_in_catalog

    def __str__(self):
        return f"""Giveaway(id={self.giveaway_id}, title={self.title}, 
        end_date={self.end_date}, is_in_catalog={self.is_in_catalog})"""
