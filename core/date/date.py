class Date:
    def __init__(self, day: int = 0, month: int = 0,  year: int = 2025):
        self.year = year
        self.month = month
        self.day = day


    def __str__(self):

        return f"{self.day}.{self.month}"