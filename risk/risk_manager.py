def calculate_position_size(
    balance,
    risk_percent,
    entry_price,
    stop_loss_price
):
    """
    Calculate position size based on the amount
    we are willing to risk.
    """

    risk_amount = balance * (risk_percent / 100)

    price_difference = abs(entry_price - stop_loss_price)

    if price_difference <= 0:
        return 0

    position_size = risk_amount / price_difference

    return position_size


def check_risk(balance, risk_percent):
    """
    Prevent excessive risk.
    """

    if risk_percent <= 0:
        return False

    if risk_percent > 2:
        return False

    return True