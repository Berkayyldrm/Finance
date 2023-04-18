
from datetime import datetime
import pandas as pd
from typing import List

def calculate_classic_pivot_points(data: pd.DataFrame, date: str) -> List[float]:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    high, low, close = filtered_data['high'], filtered_data['low'], filtered_data['close']
    pivot = (high + low + close) / 3
    resistance_1 = (2 * pivot) - low
    support_1 = (2 * pivot) - high
    resistance_2 = pivot + (high - low)
    support_2 = pivot - (high - low)
    resistance_3 = high + 2 * (pivot - low)
    support_3 = low - 2 * (high - pivot)
    print(filtered_data)
    current_price = filtered_data.loc[0, "close"] #???????????????
    print(current_price)
    return [pivot.iloc[-1], resistance_1.iloc[-1], resistance_2.iloc[-1], resistance_3.iloc[-1], support_1.iloc[-1], support_2.iloc[-1], support_3.iloc[-1], current_price]


def interpret_classic_pivot_points(classic_pivot_points: List[float], current_price: float) -> str:
    if current_price > classic_pivot_points[3]:
        return "Strong Bullish"
    elif current_price > classic_pivot_points[2] and current_price <= classic_pivot_points[3]:
        return "Bullish"
    elif current_price > classic_pivot_points[1] and current_price <= classic_pivot_points[2]:
        return "Neutral to Bullish"
    elif current_price > classic_pivot_points[0] and current_price <= classic_pivot_points[1]:
        return "Neutral"
    elif current_price > classic_pivot_points[4] and current_price <= classic_pivot_points[0]:
        return "Neutral to Bear"
    else:
        return "Bearish"