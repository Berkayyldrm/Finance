from datetime import datetime
import pandas as pd
from typing import List

def calculate_demark_pivot_points(data: pd.DataFrame, date: str, period: int) -> List[float]:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].tail(period)

    high = filtered_data["high"].max()
    low = filtered_data["low"].min()
    close = filtered_data["close"].iloc[-1]
    open_price = filtered_data["open"].iloc[-1]

    if close < open_price:
        x = high + 2 * low + close
    elif close == open_price:
        x = high + low + close
    else:
        x = 2 * high + low + close

    pivot = x / 4

    r1 = x / 2 - low
    s1 = x / 2 - high

    resistance_levels = [r1]
    support_levels = [s1]
    current_price = filtered_data.iloc[0]['close']
    return support_levels, resistance_levels, pivot, current_price


def interpret_demark_pivot_points(current_price: float, support_levels: List[float], resistance_levels: List[float], pivot: float) -> str:
    if current_price > resistance_levels[0]:
        return "Al"
    elif (current_price > pivot) and (current_price < resistance_levels[0]):
        return "Zayıf Al"
    elif (current_price < pivot) and (current_price > support_levels[0]):
        return "Zayıf Sat"
    else:
        return "Sat"