from datetime import datetime
import pandas as pd
from typing import List

def calculate_camarilla_pivot_points(data: pd.DataFrame, date: str, period: int) -> List[float]:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)

    high, low, close = filtered_data['high'], filtered_data['low'], filtered_data['close']
    pivot = close.iloc[0]
    r1 = pivot + (high.iloc[0] - low.iloc[0]) * 1.0833
    r2 = pivot + (high.iloc[0] - low.iloc[0]) * 1.1666
    r3 = pivot + (high.iloc[0] - low.iloc[0]) * 1.25

    s1 = pivot - (high.iloc[0] - low.iloc[0]) * 1.0833
    s2 = pivot - (high.iloc[0] - low.iloc[0]) * 1.1666
    s3 = pivot - (high.iloc[0] - low.iloc[0]) * 1.25

    current_price = filtered_data.iloc[0]['close']

    return [pivot, r1, r2, r3, s1, s2, s3, current_price]

def interpret_camarilla_pivot_points(camarilla_pivot_points: List[float], current_price: float) -> str:
    if current_price > camarilla_pivot_points[3]:
        return "Strong Bullish"
    elif current_price > camarilla_pivot_points[2] and current_price <= camarilla_pivot_points[3]:
        return "Bullish"
    elif current_price > camarilla_pivot_points[1] and current_price <= camarilla_pivot_points[2]:
        return "Neutral to Bullish"
    elif current_price > camarilla_pivot_points[0] and current_price <= camarilla_pivot_points[1]:
        return "Neutral"
    elif current_price > camarilla_pivot_points[6] and current_price <= camarilla_pivot_points[0]:
        return "Neutral to Bearish"
    else:
        return "Bearish"