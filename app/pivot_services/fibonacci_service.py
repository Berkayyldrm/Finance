from datetime import datetime, date
import pandas as pd
from typing import List, Tuple


def calculate_fibonacci_pivot_points(data: pd.DataFrame, date: date, period: int) -> List[float]:
    
    filtered_data = data.loc[data['date'] <= date].tail(period)

    high = filtered_data["high"].max()
    low = filtered_data["low"].min()
    close = filtered_data["close"].iloc[-1]

    pivot = (high + low + close) / 3

    r1 = pivot + (0.382 * (high - low))
    r2 = pivot + (0.618 * (high - low))
    r3 = pivot + (1 * (high - low))

    s1 = pivot - (0.382 * (high - low))
    s2 = pivot - (0.618 * (high - low))
    s3 = pivot - (1 * (high - low))

    resistance_levels = [r1, r2, r3]
    support_levels = [s1, s2, s3]
    current_price = filtered_data.iloc[0]['close']
    return support_levels, resistance_levels, pivot, current_price

def calculate_fibonacci_pivot_points_all(data: pd.DataFrame, date: date, period: int) -> List[List[float]]:
    
    filtered_data = data.loc[data['date'] <= date]

    fibonacci = []

    for i in range(0, len(filtered_data) - period + 1):
        sliced_data = filtered_data.iloc[i:i + period]

        high = sliced_data["high"].max()
        low = sliced_data["low"].min()
        close = sliced_data["close"].iloc[-1]

        pivot = (high + low + close) / 3

        r1 = pivot + (0.382 * (high - low))
        r2 = pivot + (0.618 * (high - low))
        r3 = pivot + (1 * (high - low))

        s1 = pivot - (0.382 * (high - low))
        s2 = pivot - (0.618 * (high - low))
        s3 = pivot - (1 * (high - low))

        resistance_levels = [r1, r2, r3]
        support_levels = [s1, s2, s3]
        current_price = sliced_data.iloc[0]['close']
        fibonacci.append((support_levels, resistance_levels, pivot, current_price))
    
    return fibonacci

def interpret_fibonacci_pivot_points(current_price: float, support_levels: List[float], resistance_levels: List[float], pivot: float) -> str:
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
    

def interpret_fibonacci_pivot_points_all(current_price: pd.Series, support_levels: pd.Series, resistance_levels: pd.Series, pivot: pd.Series) -> float:
    return current_price - pivot 

"""def interpret_fibonacci_pivot_points_all(current_price: pd.Series, support_levels: pd.Series, resistance_levels: pd.Series, pivot: pd.Series) -> pd.Series:
    input_df = pd.concat([current_price, support_levels, resistance_levels, pivot], axis=1)
    input_df.columns = ['current_price', 'support_levels', 'resistance_levels', 'pivot']

    return input_df.apply(lambda row: (
        "Güçlü Al" if row['current_price'] > row['resistance_levels'][1] else
        "Al" if row['current_price'] > row['resistance_levels'][0] else
        "Zayıf Al" if row['current_price'] > row['pivot'] and row['current_price'] < row['resistance_levels'][0] else
        "Zayıf Sat" if row['current_price'] < row['pivot'] and row['current_price'] > row['support_levels'][0] else
        "Sat" if row['current_price'] > row['support_levels'][1] and row['current_price'] <= row['support_levels'][0] else
        "Güçlü Sat"
    ), axis=1)"""