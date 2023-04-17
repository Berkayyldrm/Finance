import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta


def calculate_atr(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)

    # Calculate ATR manually
    high_low = filtered_data["high"] - filtered_data["low"]
    high_close = abs(filtered_data["high"] - filtered_data["close"].shift(-1))
    low_close = abs(filtered_data["low"] - filtered_data["close"].shift(-1))
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1, skipna=False)
    tr.dropna(inplace=True)
    atr = tr.rolling(period).mean().iloc[-1]
    return atr
    

def interpret_atr(atr_value: float) -> str:
    if atr_value < 0.5:
        return "Very low volatility"
    elif 0.5 <= atr_value < 1:
        return "Low volatility"
    elif 1 <= atr_value < 2:
        return "Moderate volatility"
    elif 2 <= atr_value < 4:
        return "High volatility"
    else:
        return "Very high volatility"