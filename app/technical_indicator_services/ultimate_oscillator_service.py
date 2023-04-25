import pandas_ta as ta
import pandas as pd
from datetime import datetime
def calculate_ultimate_oscillator(data: pd.DataFrame, date: str, short_period: int, medium_period: int, long_period: int) -> float:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data["date"] <= end_date]

    uo = ta.uo(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], fast=short_period, medium=medium_period, slow=long_period)

    return uo.iloc[-1]

def interpret_ultimate_oscillator(oscillator_value: float) -> str:
    if oscillator_value > 70:
        return "Güçlü Al"
    elif 50 < oscillator_value <= 70:
        return "Al"
    elif 30 < oscillator_value <= 50:
        return "Nötr"
    elif 20 < oscillator_value <= 30:
        return "Sat"
    else:
        return "Güçlü Sat"