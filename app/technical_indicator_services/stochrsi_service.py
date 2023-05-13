from datetime import datetime, date
import numpy as np
import pandas as pd
import pandas_ta as ta

def calculate_stochrsi(data: pd.DataFrame, date: date, period: int, rsi_period: int, k: int, d: int) -> float:
    
    filtered_data = data.loc[data['date'] <= date]

    stochrsi = ta.stochrsi(close=filtered_data['close'], rsi_length=rsi_period, length=period, k=k, smooth_d=d)
    stochrsi_k = stochrsi['STOCHRSIk_{}_{}_{}_{}'.format(rsi_period, period, k, d)].iloc[-1]
    stochrsi_d = stochrsi['STOCHRSId_{}_{}_{}_{}'.format(rsi_period, period, k, d)].iloc[-1]
    stochrsi_prev_k = stochrsi['STOCHRSIk_{}_{}_{}_{}'.format(rsi_period, period, k, d)].iloc[-2]
    stochrsi_prev_d = stochrsi['STOCHRSId_{}_{}_{}_{}'.format(rsi_period, period, k, d)].iloc[-2]

    return stochrsi_k, stochrsi_d, stochrsi_prev_k, stochrsi_prev_d


def calculate_stochrsi_all(data: pd.DataFrame, date: date, period: int, rsi_period: int, k: int, d: int):
    
    filtered_data = data.loc[data['date'] <= date]

    stochrsi = ta.stochrsi(close=filtered_data['close'], rsi_length=rsi_period, length=period, k=k, smooth_d=d)
    stochrsi_k = stochrsi['STOCHRSIk_{}_{}_{}_{}'.format(rsi_period, period, k, d)]
    stochrsi_d = stochrsi['STOCHRSId_{}_{}_{}_{}'.format(rsi_period, period, k, d)]
    stochrsi_prev_k = stochrsi['STOCHRSIk_{}_{}_{}_{}'.format(rsi_period, period, k, d)].shift(1)
    stochrsi_prev_d = stochrsi['STOCHRSId_{}_{}_{}_{}'.format(rsi_period, period, k, d)].shift(1)

    return stochrsi_k, stochrsi_d, stochrsi_prev_k, stochrsi_prev_d


def interpret_stochrsi(stochrsi_k: float, stochrsi_d: float, stochrsi_prev_k: float, stochrsi_prev_d: float) -> str:
    if stochrsi_k > 0.8 and stochrsi_d > 0.8 and stochrsi_prev_k > stochrsi_prev_d and stochrsi_k < stochrsi_d:
        return "Güçlü Sat"
    elif stochrsi_k < 0.2 and stochrsi_d < 0.2 and stochrsi_prev_k < stochrsi_prev_d and stochrsi_k > stochrsi_d:
        return "Güçlü Al"
    elif stochrsi_prev_k < stochrsi_prev_d and stochrsi_k > stochrsi_d:
        return "Al"
    elif stochrsi_prev_k > stochrsi_prev_d and stochrsi_k < stochrsi_d:
        return "Sat"
    else:
        return "Nötr"

def interpret_stochrsi_all(row):
    try:
        stochrsi_k = row[0]
        stochrsi_d = row[1]
        stochrsi_prev_k = row[2]
        stochrsi_prev_d = row[3]
        
        if stochrsi_k > 0.8 and stochrsi_d > 0.8 and stochrsi_prev_k > stochrsi_prev_d and stochrsi_k < stochrsi_d:
            return "Güçlü Sat"
        elif stochrsi_k < 0.2 and stochrsi_d < 0.2 and stochrsi_prev_k < stochrsi_prev_d and stochrsi_k > stochrsi_d:
            return "Güçlü Al"
        elif stochrsi_prev_k < stochrsi_prev_d and stochrsi_k > stochrsi_d:
            return "Al"
        elif stochrsi_prev_k > stochrsi_prev_d and stochrsi_k < stochrsi_d:
            return "Sat"
        else:
            return "Nötr"
        
    except Exception as e:
        return np.nan