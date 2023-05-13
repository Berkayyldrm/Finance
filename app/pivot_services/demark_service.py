from datetime import datetime, date
import pandas as pd
from typing import List

def calculate_demark_pivot_points(data: pd.DataFrame, date: date, period: int) -> List[float]:
    
    filtered_data = data.loc[data['date'] <= date].tail(period)

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

def calculate_demark_pivot_points_all(data: pd.DataFrame, date: date, period: int) -> List[List[float]]:
    
    filtered_data = data.loc[data['date'] <= date]

    demark = []

    for i in range(0, len(filtered_data) - period + 1):
        sliced_data = filtered_data.iloc[i:i + period]

        high = sliced_data["high"].max()
        low = sliced_data["low"].min()
        close = sliced_data["close"].iloc[-1]
        open_price = sliced_data["open"].iloc[-1]

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
        current_price = sliced_data.iloc[0]['close']
        demark.append((support_levels, resistance_levels, pivot, current_price))
    
    return demark

def interpret_demark_pivot_points(current_price: float, support_levels: List[float], resistance_levels: List[float], pivot: float) -> str:
    if current_price > resistance_levels[0]:
        return "Al"
    elif (current_price > pivot) and (current_price < resistance_levels[0]):
        return "Zayıf Al"
    elif (current_price < pivot) and (current_price > support_levels[0]):
        return "Zayıf Sat"
    else:
        return "Sat"

def interpret_demark_pivot_points_all(current_price: pd.Series, support_levels: pd.Series, resistance_levels: pd.Series, pivot: pd.Series) -> float:
    return current_price - pivot 
    
"""def interpret_demark_pivot_points_all(current_price: pd.Series, support_levels: pd.Series, resistance_levels: pd.Series, pivot: pd.Series) -> pd.Series:
    input_df = pd.concat([current_price, support_levels, resistance_levels, pivot], axis=1)
    input_df.columns = ['current_price', 'support_levels', 'resistance_levels', 'pivot']

    return input_df.apply(lambda row: (
        "Al" if row['current_price'] > row['resistance_levels'][0] else
        "Zayıf Al" if row['current_price'] > row['pivot'] and row['current_price'] < row['resistance_levels'][0] else
        "Zayıf Sat" if row['current_price'] < row['pivot'] and row['current_price'] > row['support_levels'][0] else
        "Sat"
    ), axis=1)"""