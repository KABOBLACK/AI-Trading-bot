class Trade:
    def __init__(
        self,
        direction,
        entry_price,
        exit_price,
        position_size,
        profit
    ):
        self.direction = direction
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.position_size = position_size
        self.profit = profit

    def to_dict(self):
        return {
            "direction": self.direction,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "position_size": self.position_size,
            "profit": self.profit
        }