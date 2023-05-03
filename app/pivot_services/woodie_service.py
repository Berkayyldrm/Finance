from datetime import datetime
import pandas as pd
from typing import List

def calculate_woodie_pivot_points(data: pd.DataFrame, date: str, period: int) -> List[float]:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].tail(period)

    high = filtered_data["high"].max()
    low = filtered_data["low"].min()
    close = filtered_data["close"].iloc[-1]

    pivot = (high + low + 2 * close) / 4

    r1 = 2 * pivot - low
    r2 = pivot + (high - low)
    r3 = high + 2 * (pivot - low)

    s1 = 2 * pivot - high
    s2 = pivot - (high - low)
    s3 = low - 2 * (high - pivot)

    resistance_levels = [r1, r2, r3]
    support_levels = [s1, s2, s3]
    current_price = filtered_data.iloc[0]['close']
    return support_levels, resistance_levels, pivot, current_price

def interpret_woodie_pivot_points(current_price: float, support_levels: List[float], resistance_levels: List[float], pivot: float) -> str:
    if current_price > resistance_levels[1]:
        return "Güçlü Al"
    elif current_price > resistance_levels[0]:
        return "Al"
    elif current_price > pivot and current_price < resistance_levels[0]:
        return "Zayıf Al"
    elif current_price < pivot and current_price > support_levels[0]:
        return "Zayıf Sat"
    elif current_price > support_levels[1] and current_price <= support_levels[0]:
        return "Sat"
    else:
        return "Güçlü Sat"