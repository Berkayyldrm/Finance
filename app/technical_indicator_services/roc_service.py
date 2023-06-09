from datetime import datetime, timedelta, date
import pandas as pd
import pandas_ta as ta

def calculate_roc(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    roc = ta.roc(filtered_data["close"], length=period)

    return roc.iloc[-1]

def calculate_roc_all(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    roc = ta.roc(filtered_data["close"], length=period)
    
    return roc

def interpret_roc(roc_value: float) -> str:
    if roc_value > 10:
        return "Güçlü Al"
    elif 5 < roc_value <= 10:
        return "Al"
    elif -5 <= roc_value <= 5:
        return "Nötr"
    elif -10 <= roc_value < -5:
        return "Sat"
    else:
        return "Güçlü Sat"