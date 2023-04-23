import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta

def calculate_hl(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].tail(period)

    # Calculate high and low values
    high = filtered_data["high"].max()
    low = filtered_data["low"].min()
    return high, low
    

def interpret_hl(high: float, low: float) -> str:
    ratio = high / low
    if ratio >= 1.1:
        return "Güçlü Al"
    elif 1.05 < ratio < 1.1:
        return "Al"
    elif 0.95 <= ratio <= 1.05:
        return "Nötr"
    elif 0.9 < ratio < 0.95:
        return "Sat"
    elif ratio <= 0.9:
        return "Güçlü Sat"