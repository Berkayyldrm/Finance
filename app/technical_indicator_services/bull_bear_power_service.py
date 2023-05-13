from datetime import datetime, timedelta, date
import pandas as pd
import pandas_ta as ta

def calculate_bull_bear_power(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]
    
    bull_power = filtered_data["high"] - ta.ema(filtered_data["close"], length=period)
    bear_power = filtered_data["low"] - ta.ema(filtered_data["close"], length=period)

    return bull_power.iloc[-1], bear_power.iloc[-1]


def calculate_bull_bear_power_all(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    bull_power = filtered_data["high"] - ta.ema(filtered_data["close"], length=period)
    bear_power = filtered_data["low"] - ta.ema(filtered_data["close"], length=period)

    return bull_power, bear_power


def interpret_bull_bear_power(bull_power: float, bear_power: float) -> str:
    if bull_power > 0 and bear_power < 0:
        return "Güçlü Al"
    elif bull_power < 0 and bear_power > 0:
        return "Güçlü Sat"
    elif bull_power > 0 and bear_power > 0:
        return "Al"
    elif bull_power < 0 and bear_power < 0:
        return "Sat"
    else:
        return "Nötr"