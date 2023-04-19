from datetime import datetime
import pandas as pd
from typing import List

def calculate_demark_pivot_points(data: pd.DataFrame, date: str, period: int) -> List[float]:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)

    high, low, close = filtered_data['high'], filtered_data['low'], filtered_data['close']

    x = high.iloc[-1] + 2 * low.iloc[-1] + close.iloc[-1]
    y = 2 * high.iloc[-1] - low.iloc[-1] - close.iloc[-1]
    z = close.iloc[-1] + 2 * low.iloc[-1] + high.iloc[-1]

    if x >= y and x >= z:
        pivot = (x + 2 * low.iloc[-1] + close.iloc[-1]) / 4
    elif y >= x and y >= z:
        pivot = (y + 2 * high.iloc[-1] - low.iloc[-1]) / 4
    elif z >= x and z >= y:
        pivot = (z + 2 * high.iloc[-1] + close.iloc[-1]) / 4

    r1 = pivot + high.iloc[-1] - low.iloc[-1]
    s1 = pivot - high.iloc[-1] + low.iloc[-1]

    current_price = filtered_data.iloc[-1]['close']
    
    return [pivot, r1, s1, current_price]


def interpret_demark_pivot_points(demark_pivot_points: List[float], current_price: float) -> str:
    if current_price > demark_pivot_points[1]:
        return "Bullish"
    elif current_price < demark_pivot_points[2]:
        return "Bearish"
    else:
        return "Neutral"