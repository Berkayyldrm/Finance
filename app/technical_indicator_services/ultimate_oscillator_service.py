import pandas_ta as ta
import pandas as pd
from datetime import datetime
def calculate_ultimate_oscillator(data: pd.DataFrame, date: str, fast_period: int = 7, mid_period: int = 14, slow_period: int = 28) -> float:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data["date"] <= end_date]
    print(filtered_data)
    true_range = ta.true_range(filtered_data["high"], filtered_data["low"], filtered_data["close"])
    buying_pressure = filtered_data["close"] - filtered_data["low"]
  
    fast_bp = buying_pressure.rolling(fast_period).sum()
    mid_bp = buying_pressure.rolling(mid_period).sum()
    slow_bp = buying_pressure.rolling(slow_period).sum()

    fast_tr = true_range.rolling(fast_period).sum()
    mid_tr = true_range.rolling(mid_period).sum()
    slow_tr = true_range.rolling(slow_period).sum()

    uo = (4 * fast_bp / fast_tr) + (2 * mid_bp / mid_tr) + (slow_bp / slow_tr)
    uo = uo / (4 + 2 + 1)

    return uo.iloc[-1]

def interpret_ultimate_oscillator(oscillator_value: float) -> str:
    if oscillator_value > 70:
        return "Güçlü Sat"
    elif 50 < oscillator_value <= 70:
        return "Sat"
    elif 30 < oscillator_value <= 50:
        return "Nötr"
    elif 20 < oscillator_value <= 30:
        return "Al"
    else:
        return "Güçlü Al"