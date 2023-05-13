from datetime import datetime, date
import numpy as np
import pandas as pd
import pandas_ta as ta

def calculate_macd(data: pd.DataFrame, date: date, fast_period: int, slow_period: int, signal_period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    macd = ta.macd(filtered_data["close"], fast=fast_period, slow=slow_period, signal=signal_period)
    macd_ = macd[f'MACD_{fast_period}_{slow_period}_{signal_period}'].iloc[-1]
    macd_h = macd[f'MACDh_{fast_period}_{slow_period}_{signal_period}'].iloc[-1]
    macd_s = macd[f'MACDs_{fast_period}_{slow_period}_{signal_period}'].iloc[-1]
    macd_prev = macd[f'MACD_{fast_period}_{slow_period}_{signal_period}'].iloc[-2]
    macd_s_prev = macd[f'MACDs_{fast_period}_{slow_period}_{signal_period}'].iloc[-2]

    return macd_, macd_h, macd_s, macd_prev, macd_s_prev

def calculate_macd_all(data: pd.DataFrame, date: date, fast_period: int, slow_period: int, signal_period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    macd = ta.macd(filtered_data["close"], fast=fast_period, slow=slow_period, signal=signal_period)
    macd_ = macd[f'MACD_{fast_period}_{slow_period}_{signal_period}']
    macd_h = macd[f'MACDh_{fast_period}_{slow_period}_{signal_period}']
    macd_s = macd[f'MACDs_{fast_period}_{slow_period}_{signal_period}']
    macd_prev = macd[f'MACD_{fast_period}_{slow_period}_{signal_period}'].shift(1)
    macd_s_prev = macd[f'MACDs_{fast_period}_{slow_period}_{signal_period}'].shift(1)

    return macd_, macd_h, macd_s, macd_prev, macd_s_prev



def interpret_macd(macd: float, macd_h: float, macd_s: float, macd_prev: float, macd_s_prev: float) -> str:
    if macd_h > 0 and macd_prev < macd_s_prev and macd > macd_s:
        return "Güçlü Al"
    elif macd_h < 0 and macd_prev > macd_s_prev and macd < macd_s:
        return "Güçlü Sat"
    elif macd_prev < macd_s_prev and macd > macd_s:
        return "Al"
    elif macd_prev > macd_s_prev and macd < macd_s:
        return "Sat"
    else:
        return "Nötr"

def interpret_macd_all(row):
    try:
        macd = row[0]
        macd_h = row[1]
        macd_s = row[2]
        macd_prev = row[3]
        macd_s_prev = row[4]
        
        if macd_h > 0 and macd_prev < macd_s_prev and macd > macd_s:
            return "Güçlü Al"
        elif macd_h < 0 and macd_prev > macd_s_prev and macd < macd_s:
            return "Güçlü Sat"
        elif macd_prev < macd_s_prev and macd > macd_s:
            return "Al"
        elif macd_prev > macd_s_prev and macd < macd_s:
            return "Sat"
        else:
            return "Nötr"
        
    except Exception as e:
        return np.nan