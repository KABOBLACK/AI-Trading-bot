from strategy.strategy import generate_signal
from risk.risk_manager import calculate_position_size, check_risk


class TradingBot:

    def __init__(self, balance=1000, risk_percent=1):
        self.balance = balance
        self.risk_percent = risk_percent
        self.position = None

    def analyze(self, data):
        """Analyze market data and generate a signal."""

        signal = generate_signal(data)

        if signal == "BUY":
            return self.open_trade(data, "BUY")

        if signal == "SELL":
            return self.open_trade(data, "SELL")

        return {
            "signal": "HOLD",
            "message": "No trade opportunity"
        }

    def open_trade(self, data, direction):
        """Prepare a trade after checking risk."""

        entry_price = data["close"].iloc[-1]

        if direction == "BUY":
            stop_loss = entry_price * 0.99
        else:
            stop_loss = entry_price * 1.01

        if not check_risk(self.balance, self.risk_percent):
            return {
                "signal": direction,
                "status": "REJECTED",
                "message": "Risk limit exceeded"
            }

        position_size = calculate_position_size(
            self.balance,
            self.risk_percent,
            entry_price,
            stop_loss
        )

        self.position = {
            "direction": direction,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "position_size": position_size
        }

        return {
            "signal": direction,
            "status": "PAPER_TRADE",
            "position": self.position
        }