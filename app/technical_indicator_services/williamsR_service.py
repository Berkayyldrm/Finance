from typing import List
from app.models.data import BorsaData
from datetime import datetime, timedelta
from app.services.data_service import get_all_data
from datetime import date

def calculate_williams_r(filtered_data: List[BorsaData], date: date, period: int = 14) -> float:
    date = datetime.strptime(date, "%Y-%m-%d").date()

    # Filter the prices for the specified period
    start_date = date - timedelta(days=period)
    end_date = date - timedelta(days=1)

    filtered_prices = [price for price in filtered_data if start_date <= price.date <= end_date]

    # Calculate the highest high and lowest low for the past period days
    highest_high = max([price.high for price in filtered_prices])
    lowest_low = min([price.low for price in filtered_prices])

    # Calculate Williams %R
    current_price = filtered_data[-1].close
    wr = ((highest_high - current_price) / (highest_high - lowest_low)) * -100

    return wr

def interpret_williams_r(williams_r: float) -> str:
    if williams_r < -80:
        return "Aşırı Satım Bölgesi"
    elif -80 <= williams_r < -50:
        return "Fiyatların Artması Beklenir"
    elif -50 <= williams_r < -20:
        return "Fiyatların Hız Kazandığı Bölge"
    elif -20 <= williams_r < 0:
        return "Aşırı Alım Bölgesi"
    else:
        return "Fiyatların Düşmesi Beklenir"