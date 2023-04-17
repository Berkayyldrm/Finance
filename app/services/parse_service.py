from datetime import datetime
from app.models.data import BorsaData
def parse_data(data: tuple):
    data = "*".join(str(item) for item in data)
    fields = data.split("*")
    date_str = fields[0]
    date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
    close_price = float(fields[1].replace(",", "."))
    open_price = float(fields[2].replace(",", "."))
    high_price = float(fields[3].replace(",", "."))
    low_price = float(fields[4].replace(",", "."))
    volume_str = fields[5].replace(",", ".").rstrip("M").rstrip("K")
    if volume_str:
        if volume_str.endswith("M"):
            volume = float(volume_str[:-1]) * 1000000
        elif volume_str.endswith("K"):
            volume = float(volume_str[:-1]) * 1000
        else:
            volume = float(volume_str)
    else:
        volume = 0.0
    percentage_str = fields[6].replace(",", ".").rstrip("%")
    if percentage_str:
        percentage = float(percentage_str)
    else:
        percentage = 0.0
    return BorsaData(
        date=date_obj,
        open=open_price,
        high=high_price,
        low=low_price,
        close=close_price,
        volume=volume,
        percentage=percentage,
    )