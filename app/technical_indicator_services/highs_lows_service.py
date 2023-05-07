import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta, date

def calculate_hl(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date].tail(period)

    high_count = 0
    low_count = 0
    
    for index, row in filtered_data.iterrows():
        previous_index = index - 1
        if previous_index in filtered_data.index:
            previous_row = filtered_data.loc[previous_index]
            if row["high"] > previous_row["high"]:
                high_count += 1
            if row["low"] < previous_row["low"]:
                low_count += 1
    ratio = 100 * high_count / (high_count + low_count)    
      
    return ratio

def calculate_hl_all(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]
    
    hl_ratios = []

    for index, row in filtered_data.iterrows():
        window_start = index - period + 1
        if window_start >= 0:
            window_data = filtered_data.iloc[window_start:index + 1]

            high_count = 0
            low_count = 0

            for i, current_row in window_data.iterrows():
                previous_index = i - 1
                if previous_index in window_data.index:
                    previous_row = window_data.loc[previous_index]
                    if current_row["high"] > previous_row["high"]:
                        high_count += 1
                    if current_row["low"] < previous_row["low"]:
                        low_count += 1

            ratio = 100 * high_count / (high_count + low_count)
            hl_ratios.append(ratio)

    return hl_ratios
    

def interpret_hl(ratio: float) -> str:
    if ratio >= 70:
        return "Güçlü Al"
    elif 50 < ratio < 70:
        return "Al"
    elif 30 < ratio < 50:
        return "Sat"
    elif ratio <= 30:
        return "Güçlü Sat"