import pandas as pd
import pandas_ta as ta
from datetime import datetime, date

def calculate_cci(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    cci = ta.cci(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], length=period)

    return cci.iloc[-1]

def calculate_cci_all(data: pd.DataFrame, date: date, period: int) -> float:
    
    filtered_data = data.loc[data['date'] <= date]

    cci = ta.cci(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], length=period)

    return cci


def interpret_cci(cci):
    if cci > 200:
        return "Güçlü Al"
    elif 100 < cci <= 200:
        return "Al"
    elif -100 <= cci <= 100:
        return "Nötr"
    elif -200 <= cci < -100:
        return "Sat"
    else:
        return "Güçlü Sat"