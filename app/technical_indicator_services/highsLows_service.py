import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta

def calculate_hl(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)

    # Calculate high and low values
    high = filtered_data["high"].max()
    low = filtered_data["low"].min()
    return high, low
    

def interpret_hl(high: float, low: float) -> str:
    if high > 1.1 * low:
        return "Strong buy"
    elif 1.05 * low < high <= 1.1 * low:
        return "Buy"
    elif 0.95 * low <= high <= 1.05 * low:
        return "Neutral"
    elif 1.1 * high >= low > 1.05 * high:
        return "Sell"
    elif low > 1.1 * high:
        return "Strong sell"
    else:
        return "Undefined"