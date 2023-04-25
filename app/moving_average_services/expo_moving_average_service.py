from datetime import datetime
import pandas_ta as ta
import pandas as pd

def calculate_expo_moving_average(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    ema = ta.ema(filtered_data["close"], length=period)
    current_price = data.loc[data['date'] == end_date, "close"].values

    return ema.iloc[-1], current_price

def interpret_expo_moving_average(ma_value: float, current_price: float) -> str:
    if current_price > ma_value * 1.05:
        return "Güçlü Al"
    elif current_price > ma_value and current_price <= ma_value * 1.05:
        return "Al"
    elif current_price >= ma_value * 0.95 and current_price <= ma_value * 1.05:
        return "Nötr"
    elif current_price < ma_value and current_price >= ma_value * 0.95:
        return "Sat"
    else:
        return "Güçlü Sat"