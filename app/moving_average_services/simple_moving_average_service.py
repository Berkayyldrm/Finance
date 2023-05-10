from datetime import datetime
import pandas_ta as ta
import pandas as pd

def calculate_simple_moving_average(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    ma = ta.sma(filtered_data["close"], length=period)

    current_price = data.loc[data['date'] == end_date, "close"].values

    return ma.iloc[-1], current_price

def calculate_simple_moving_average_all(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    ma = ta.sma(filtered_data["close"], length=period)

    current_price = data["close"]

    return ma, current_price

def interpret_simple_moving_average(ma_value: float, current_price: float) -> str:
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
    
def interpret_simple_moving_average_all(ma_value: pd.Series, current_price: pd.Series) -> float:
    return current_price - ma_value

"""def interpret_simple_moving_average_all(ma_value: pd.Series, current_price: pd.Series) -> str:
    return ma_value.combine(current_price, lambda ma, cp: (
        "Güçlü Al" if cp > ma * 1.05 else
        "Al" if cp > ma and cp <= ma * 1.05 else
        "Nötr" if cp >= ma * 0.95 and cp <= ma * 1.05 else
        "Sat" if cp < ma and cp >= ma * 0.95 else
        "Güçlü Sat"
    ))"""