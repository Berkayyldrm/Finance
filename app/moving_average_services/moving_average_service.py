from datetime import datetime
import pandas_ta as ta
import pandas as pd

def calculate_moving_average(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)
    print(filtered_data)
    ma = ta.sma(filtered_data["close"], length=period)
    print(data.loc[data['date'] == end_date, "close"].values)
    current_price = data.loc[data['date'] == end_date, "close"].values

    return ma.iloc[-1], current_price

def interpret_moving_average(ma_value: float, current_price: float) -> str:
    if current_price > ma_value * 1.05:
        return "Strongly Bullish"
    elif current_price > ma_value and current_price <= ma_value * 1.05:
        return "Bullish"
    elif current_price >= ma_value * 0.95 and current_price <= ma_value * 1.05:
        return "Neutral"
    elif current_price < ma_value and current_price >= ma_value * 0.95:
        return "Bearish"
    else:
        return "Strongly Bearish"