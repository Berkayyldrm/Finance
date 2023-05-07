import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta, date


def calculate_atr(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    atr = ta.atr(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], length=period)
    atr = atr.iloc[-1]
    current_price = filtered_data.loc[filtered_data["date"] == date, "close"].values[0]
    percentage_atr = (atr / current_price) * 100
    
    return atr, percentage_atr


def calculate_atr_all(data: pd.DataFrame, date: str, period: int) -> float:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    atr = ta.atr(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], length=period)
    
    return atr
    

def interpret_atr(percentage_atr: float) -> str:
    
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