from datetime import datetime
import pandas as pd
from typing import List

def calculate_camarilla_pivot_points(data: pd.DataFrame, date: str, period: int) -> List[float]:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].tail(period)

    high = filtered_data["high"].max()
    low = filtered_data["low"].min()
    close = filtered_data["close"].iloc[-1]

    pivot = (high + low + close) / 3

    range_ = high - low

    r1 = close + (1.1/12) * range_
    r2 = close + (1.1/6) * range_
    r3 = close + (1.1/4) * range_

    s1 = close - (1.1/12) * range_
    s2 = close - (1.1/6) * range_
    s3 = close - (1.1/4) * range_

    resistance_levels = [r1, r2, r3]
    support_levels = [s1, s2, s3]
    current_price = filtered_data.iloc[0]['close']
    return support_levels, resistance_levels, pivot, current_price

def calculate_camarilla_pivot_points_all(data: pd.DataFrame, date: str, period: int) -> List[List[float]]:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    camarilla = []

    for i in range(0, len(filtered_data) - period + 1):
        sliced_data = filtered_data.iloc[i:i + period]

        high = sliced_data["high"].max()
        low = sliced_data["low"].min()
        close = sliced_data["close"].iloc[-1]

        pivot = (high + low + close) / 3

        range_ = high - low

        r1 = close + (1.1/12) * range_
        r2 = close + (1.1/6) * range_
        r3 = close + (1.1/4) * range_

        s1 = close - (1.1/12) * range_
        s2 = close - (1.1/6) * range_
        s3 = close - (1.1/4) * range_

        resistance_levels = [r1, r2, r3]
        support_levels = [s1, s2, s3]
        current_price = sliced_data.iloc[0]['close']
        camarilla.append((support_levels, resistance_levels, pivot, current_price))
    
    return camarilla

def interpret_camarilla_pivot_points(current_price: float, support_levels: List[float], resistance_levels: List[float], pivot: float) -> str:
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
    
def interpret_camarilla_pivot_points_all(current_price: pd.Series, support_levels: pd.Series, resistance_levels: pd.Series, pivot: pd.Series) -> pd.Series:
    input_df = pd.concat([current_price, support_levels, resistance_levels, pivot], axis=1)
    input_df.columns = ['current_price', 'support_levels', 'resistance_levels', 'pivot']

    return input_df.apply(lambda row: (
        "Güçlü Al" if row['current_price'] > row['resistance_levels'][1] else
        "Al" if row['current_price'] > row['resistance_levels'][0] else
        "Zayıf Al" if row['current_price'] > row['pivot'] and row['current_price'] < row['resistance_levels'][0] else
        "Zayıf Sat" if row['current_price'] < row['pivot'] and row['current_price'] > row['support_levels'][0] else
        "Sat" if row['current_price'] > row['support_levels'][1] and row['current_price'] <= row['support_levels'][0] else
        "Güçlü Sat"
    ), axis=1)