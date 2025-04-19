import os

class CoreDB():
    def __init__(self, db_name: str = "data.db"):
        self.db_name = os.path.join(os.path.dirname("db/core_db"), db_name)