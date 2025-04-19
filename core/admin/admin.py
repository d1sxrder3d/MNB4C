# core/admins/admin.py
from core.date.date import Date
from typing import Optional

class Subscription:
    class SubscriptionLevel:
        NONE = 0
        BASIC = 1
        PREMIUM = 2
        ULTIMATE = 3

    def __init__(
            self,
            subscriptin_end_time: Date = Date(),
            subscriptin_level: int = SubscriptionLevel.NONE # Изменено здесь
    ):
        self.subscriptin_level = subscriptin_level
        self.subscriptin_end_time = subscriptin_end_time

    def __str__(self):
        if self.subscriptin_level == Subscription.SubscriptionLevel.NONE:
            return f"NONE"
        return f"{self.subscriptin_level},{self.subscriptin_end_time}"

    @staticmethod
    def from_string(subscription_str: str):
        if subscription_str == "NONE":
            return Subscription()
        subscriptin_level_str, subscriptin_end_time_str = subscription_str.split(',')
        subscriptin_level = int(subscriptin_level_str)
        day, month = map(int, subscriptin_end_time_str.split('.'))
        subscriptin_end_time = Date(day=day, month=month)
        return Subscription(subscriptin_end_time, subscriptin_level) # Изменено здесь


class Admin:
    def __init__(
            self,
            user_id: int,
            user_name: str,
            subscription: Subscription = Subscription(),
            giveaways: list = []

    ):
        self.user_id = user_id
        self.user_name = user_name
        self.subscription = subscription
        self.giveaways = giveaways

    def add_giveaway(self, giveaway_id):
        
        self.giveaways.append(giveaway_id)

    def subscribe(self, subscription):
        self.subscription = subscription
