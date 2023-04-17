from typing import List
from app.models.data import BorsaData
from datetime import datetime, timedelta
from app.services.data_service import get_all_data
from datetime import date

def calculate_stoch(filtered_data: List[BorsaData], date: date, period: int = 14, slow_period: int = 6) -> float:
    # Calculate the highest high and lowest low for the past period days

    date = datetime.strptime(date, "%Y-%m-%d").date()

    # Filter the prices for the specified period
    start_date = date - timedelta(days=period)
    end_date = date - timedelta(days=1)

    filtered_data = [price for price in filtered_data if start_date <= price.date <= end_date]

    highs = [d.high for d in filtered_data[-period:]]
    highest_high = max(highs)
    lows = [d.low for d in filtered_data[-period:]]
    lowest_low = min(lows)

    # Calculate the %K value
    current_price = filtered_data[-1].close
    k_value = ((current_price - lowest_low) / (highest_high - lowest_low)) * 100

    # Calculate the %D value (slow %K)
    prev_k_values = [((d.close - min(lows[-slow_period:])) / (max(highs[-slow_period:]) - min(lows[-slow_period:]))) * 100 for d in filtered_data[-slow_period - period:-slow_period]]
    d_value = sum(prev_k_values) / len(prev_k_values)

    return k_value, d_value # d_value - > sma_d_value

def interpret_stoch(k_value: float, d_value: float) -> str:
    if k_value > d_value:
        return "Overbought"
    else:
        return "Oversold"