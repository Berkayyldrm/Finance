import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta

def calculate_hl(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].tail(period)
    # Calculate high and low values
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
    

def interpret_hl(ratio: float) -> str:
    if ratio >= 70:
        return "Güçlü Al"
    elif 50 < ratio < 70:
        return "Al"
    elif 30 < ratio < 50:
        return "Sat"
    elif ratio <= 30:
        return "Güçlü Sat"