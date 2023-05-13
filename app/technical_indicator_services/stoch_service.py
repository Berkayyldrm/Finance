from datetime import datetime, date
import numpy as np
import pandas as pd
import pandas_ta as ta

def calculate_stoch(data: pd.DataFrame, date: date, k: int, d: int, smooth_k: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    stoch = ta.stoch(filtered_data["high"], filtered_data["low"], filtered_data["close"], k=k, d=d, smooth_k=smooth_k)
    stoch_k = stoch['STOCHk_{}_{}_{}'.format(k, d, smooth_k)].iloc[-1]
    stoch_d = stoch['STOCHd_{}_{}_{}'.format(k, d, smooth_k)].iloc[-1]
    stoch_prev_k = stoch['STOCHk_{}_{}_{}'.format(k, d, smooth_k)].iloc[-2]
    stoch_prev_d = stoch['STOCHd_{}_{}_{}'.format(k, d, smooth_k)].iloc[-2]

    return stoch_k, stoch_d, stoch_prev_k, stoch_prev_d


def calculate_stoch_all(data: pd.DataFrame, date: date, k: int, d: int, smooth_k: int):

    filtered_data = data.loc[data['date'] <= date]

    stoch = ta.stoch(filtered_data["high"], filtered_data["low"], filtered_data["close"], k=k, d=d, smooth_k=smooth_k)
    stoch_k = stoch['STOCHk_{}_{}_{}'.format(k, d, smooth_k)]
    stoch_d = stoch['STOCHd_{}_{}_{}'.format(k, d, smooth_k)]
    stoch_prev_k = stoch['STOCHk_{}_{}_{}'.format(k, d, smooth_k)].shift(1)
    stoch_prev_d = stoch['STOCHd_{}_{}_{}'.format(k, d, smooth_k)].shift(1)

    return stoch_k, stoch_d, stoch_prev_k, stoch_prev_d


def interpret_stoch(stoch_k: float, stoch_d: float, stoch_prev_k: float, stoch_prev_d: float) -> str:
    if stoch_k > 80 and stoch_d > 80 and stoch_prev_k > stoch_prev_d and stoch_k < stoch_d:
        return "Güçlü Sat"
    elif stoch_k < 20 and stoch_d < 20 and stoch_prev_k < stoch_prev_d and stoch_k > stoch_d:
        return "Güçlü Al"
    elif stoch_prev_k < stoch_prev_d and stoch_k > stoch_d:
        return "Al"
    elif stoch_prev_k > stoch_prev_d and stoch_k < stoch_d:
        return "Sat"
    else:
        return "Nötr"
    
def interpret_stoch_all(row):
    try:
        stoch_k = row[0]
        stoch_d = row[1]
        stoch_prev_k = row[2]
        stoch_prev_d = row[3]
        
        if stoch_k > 80 and stoch_d > 80 and stoch_prev_k > stoch_prev_d and stoch_k < stoch_d:
            return "Güçlü Sat"
        elif stoch_k < 20 and stoch_d < 20 and stoch_prev_k < stoch_prev_d and stoch_k > stoch_d:
            return "Güçlü Al"
        elif stoch_prev_k < stoch_prev_d and stoch_k > stoch_d:
            return "Al"
        elif stoch_prev_k > stoch_prev_d and stoch_k < stoch_d:
            return "Sat"
        else:
            return "Nötr"
        
    except Exception as e:
        return np.nan