import csv
import os


def save_trades(trades, filename="data/trade_history.csv"):
    """
    Save completed trades to a CSV file.
    """

    if not trades:
        return

    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True
    )

    fieldnames = [
        "direction",
        "entry_price",
        "exit_price",
        "position_size",
        "profit",
        "exit_reason",
        "fees"
    ]

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for trade in trades:
            writer.writerow(trade)