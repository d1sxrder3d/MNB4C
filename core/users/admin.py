from core.date.date import Date



class Subscription:
    class SubscriptionLevel:
        NONE = 0
        BASIC = 1
        PREMIUM = 2
        ULTIMATE = 3
        
    def __init__(
            self, 
            subscriptin_end_time: Date = None,
            subscriptin_level: SubscriptionLevel = SubscriptionLevel.NONE
    ):
        
        self.subscriptin_level = subscriptin_level
        self.subscriptin_end_time = subscriptin_end_time

    def __str__(self):
        if self.subscriptin_level == 0:
            return f"Подписка не оформлена"
        return f"Подписка: {self.subscription_level}, до {self.subscriptin_end_time}"
        
        


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
    def add_giveaway(self, giveaway):
        self.giveaways.append(giveaway)
    def subscribe(self, subscription):
        self.subscription = subscription