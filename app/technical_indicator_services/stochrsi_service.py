from datetime import datetime
import pandas as pd
import pandas_ta as ta

def calculate_stochrsi(data: pd.DataFrame, date: str, period: int, rsi_period: int, k: int, d: int) -> float:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    stochrsi = ta.stochrsi(close=filtered_data['close'], rsi_length=rsi_period, length=period, k=k, smooth_d=d)

    return stochrsi['STOCHRSIk_{}_{}_{}_{}'.format(rsi_period, period, k, d)].iloc[-1], stochrsi['STOCHRSId_{}_{}_{}_{}'.format(rsi_period, period, k, d)].iloc[-1]


def calculate_stochrsi_all(data: pd.DataFrame, date: str, period: int, rsi_period: int, k: int, d: int) -> float:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    stochrsi = ta.stochrsi(close=filtered_data['close'], rsi_length=rsi_period, length=period, k=k, smooth_d=d)

    return stochrsi['STOCHRSIk_{}_{}_{}_{}'.format(rsi_period, period, k, d)], stochrsi['STOCHRSId_{}_{}_{}_{}'.format(rsi_period, period, k, d)]


def interpret_stochrsi(stochrsi_k: float, stochrsi_d: float) -> str:
    if stochrsi_k > 80 and stochrsi_d > 80:
        return "Güçlü Al"
    elif stochrsi_k < 20 and stochrsi_d < 20:
        return "Güçlü Sat"
    elif stochrsi_k > stochrsi_d:
        return "Al"
    elif stochrsi_k < stochrsi_d:
        return "Sat"
    else:
        return "Nötr"