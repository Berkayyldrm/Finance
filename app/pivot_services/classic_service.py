
from datetime import datetime
import pandas as pd
from typing import List

def calculate_classic_pivot_points(data: pd.DataFrame, date: str, period: int) -> List[float]:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)
    print(filtered_data)
    high, low, close = filtered_data['high'], filtered_data['low'], filtered_data['close']
    pivot = round((high + low + close) / 3, 3)
    r1 = round((2 * pivot) - low, 3)
    s1 = round((2 * pivot) - high, 3)
    r2 = round(pivot + (high - low), 3)
    s2 = round(pivot - (high - low), 3)
    r3 = round(high + 2 * (pivot - low), 3)
    s3 = round(low - 2 * (high - pivot), 3)

    current_price = filtered_data.iloc[0]['close']

    return [pivot, r1, r2, r3, s1, s2, s3, current_price]


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