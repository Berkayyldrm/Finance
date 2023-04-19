from datetime import datetime
import pandas as pd
from typing import List

def calculate_woodie_pivot_points(data: pd.DataFrame, date: str, period: int) -> List[float]:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)

    high, low, close = filtered_data['high'], filtered_data['low'], filtered_data['close']
    pivot = (high.iloc[0] + low.iloc[0] + 2 * close.iloc[0]) / 4
    r1 = pivot + (high.iloc[0] - low.iloc[0])
    s1 = pivot - (high.iloc[0] - low.iloc[0])
    r2 = pivot + 2 * (high.iloc[0] - low.iloc[0])
    s2 = pivot - 2 * (high.iloc[0] - low.iloc[0])
    r3 = high.iloc[0] + 2 * (pivot - low.iloc[0])
    s3 = low.iloc[0] - 2 * (high.iloc[0] - pivot)

    current_price = filtered_data.iloc[0]['close']
    
    return [pivot, r1, r2, r3, s1, s2, s3, current_price]

def interpret_woodie_pivot_points(woodie_pivot_points: List[float], current_price: float) -> str:
    if current_price > woodie_pivot_points[1]:
        return "Strong Bullish"
    elif current_price > woodie_pivot_points[0] and current_price <= woodie_pivot_points[1]:
        return "Bullish"
    elif current_price > woodie_pivot_points[3] and current_price <= woodie_pivot_points[0]:
        return "Neutral to Bullish"
    elif current_price > woodie_pivot_points[4] and current_price <= woodie_pivot_points[3]:
        return "Neutral to Bearish"
    elif current_price <= woodie_pivot_points[4]:
        return "Bearish"