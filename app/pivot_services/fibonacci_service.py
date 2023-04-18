from datetime import datetime
import pandas as pd
from typing import List


def calculate_fibonacci_pivot_points(data: pd.DataFrame, date: str, period: int) -> List[float]:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)

    high, low, close = filtered_data['high'], filtered_data['low'], filtered_data['close']
    pivot = (high.iloc[0] + low.iloc[0] + close.iloc[0]) / 3
    r1 = pivot + (high.iloc[0] - low.iloc[0]) * 0.382
    r2 = pivot + (high.iloc[0] - low.iloc[0]) * 0.618
    r3 = pivot + (high.iloc[0] - low.iloc[0]) * 1
    s1 = pivot - (high.iloc[0] - low.iloc[0]) * 0.382
    s2 = pivot - (high.iloc[0] - low.iloc[0]) * 0.618
    s3 = pivot - (high.iloc[0] - low.iloc[0]) * 1

    current_price = filtered_data.iloc[0]['close']
    
    return [pivot, r1, r2, r3, s1, s2, s3, current_price]

def interpret_fibonacci_pivot_points(fibonacci_pivot_points: List[float], current_price: float) -> str:
    if current_price > fibonacci_pivot_points[3]:
        return "Strong Bullish"
    elif current_price > fibonacci_pivot_points[2] and current_price <= fibonacci_pivot_points[3]:
        return "Bullish"
    elif current_price > fibonacci_pivot_points[1] and current_price <= fibonacci_pivot_points[2]:
        return "Neutral to Bullish"
    elif current_price > fibonacci_pivot_points[0] and current_price <= fibonacci_pivot_points[1]:
        return "Neutral"
    elif current_price > fibonacci_pivot_points[4] and current_price <= fibonacci_pivot_points[0]:
        return "Neutral to Bearish"
    else:
        return "Bearish"