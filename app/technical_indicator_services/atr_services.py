import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta


def calculate_atr(data: pd.DataFrame, date: str, period: int = 14) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].tail(period+1)
    # Calculate ATR manually
    high_low = filtered_data["high"] - filtered_data["low"]
    high_close = abs(filtered_data["high"] - filtered_data["close"].shift(1))
    low_close = abs(filtered_data["low"] - filtered_data["close"].shift(1))
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1, skipna=False)
    tr.dropna(inplace=True)
    atr = tr.rolling(period).mean().iloc[-1]

    current_price = filtered_data.loc[filtered_data["date"] == end_date, "close"].values[0]

    return atr, current_price
    

def interpret_atr(atr_value: float, current_price: float) -> str:
    
    percentage_atr = (atr_value / current_price) * 100
 
    if percentage_atr > 5:
        return "Çok Yüksek Oynaklık"
    elif 3 < percentage_atr <= 5:
        return "Yüksek Oynaklık"
    elif 1 < percentage_atr <= 3:
        return "Orta Oynaklık"
    elif 0.5 < percentage_atr <= 1:
        return "Düşük Oynaklık"
    else:
        return "Çok Düşük Oynaklık"