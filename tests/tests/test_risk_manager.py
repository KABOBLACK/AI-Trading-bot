from risk.risk_manager import (
    calculate_position_size,
    check_risk
)


def test_position_size():

    position_size = calculate_position_size(
        balance=1000,
        risk_percent=1,
        entry_price=100,
        stop_loss_price=99
    )

    assert position_size == 10


def test_risk_limit_allows_one_percent():

    assert check_risk(
        balance=1000,
        risk_percent=1
    ) is True


def test_risk_limit_rejects_excessive_risk():

    assert check_risk(
        balance=1000,
        risk_percent=5
    ) is False