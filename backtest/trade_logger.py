import csv
import os


def save_trades(trades, filename="data/trade_history.csv"):
    """
    Save completed trades to a CSV file. Appends by default and writes header
    only when the file is newly created.
    """

    if not trades:
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    fieldnames = [
        "direction",
        "entry_price",
        "exit_price",
        "position_size",
        "profit",
        "exit_reason",
        "fees"
    ]

    write_header = not os.path.exists(filename)

    # Append so we keep a cumulative history; change to 'w' if you want overwrite
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        for trade in trades:
            # Ensure only known fields are written
            row = {k: trade.get(k, "") for k in fieldnames}
            writer.writerow(row)
