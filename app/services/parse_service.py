from datetime import datetime
from app.models.data import BorsaData

def parse_data(data: tuple):
    data = "*".join(str(item) for item in data)
    fields = data.split("*")

    date = fields[0]
    open_price = float(fields[1].replace(",", "."))
    high_price = float(fields[2].replace(",", "."))
    low_price = float(fields[3].replace(",", "."))
    close_price = float(fields[4].replace(",", "."))
    volume = fields[5]
    dividend = float(fields[6])
    stock_split = float(fields[7])
    percentage = float(fields[8])

    if percentage == "None":
        percentage = 0.0

    return BorsaData(
        date=date,
        open=open_price,
        high=high_price,
        low=low_price,
        close=close_price,
        volume=volume,
        percentage=percentage,
        dividend=dividend,
        stock_split=stock_split
    )