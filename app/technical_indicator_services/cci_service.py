import pandas as pd
import pandas_ta as ta
from datetime import datetime

def calculate_cci(data: pd.DataFrame, date: str, period: int = 14) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    # Calculate CCI value
    cci = ta.cci(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], window=period)

    return cci.iloc[-1]


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