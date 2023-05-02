from datetime import datetime
import pandas as pd
import pandas_ta as ta

def calculate_stoch(data: pd.DataFrame, date: str, k: int, d: int, smooth_k: int) -> tuple:
    # Calculate the highest high and lowest low for the past period days

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]
    stoch = ta.stoch(filtered_data["high"], filtered_data["low"], filtered_data["close"], k=k, d=d, smooth_k=smooth_k)
    stoch_k = stoch['STOCHk_{}_{}_{}'.format(k, d, smooth_k)].iloc[-1]
    stoch_d = stoch['STOCHd_{}_{}_{}'.format(k, d, smooth_k)].iloc[-1]
    stoch_diff = stoch_k - stoch_d
    return stoch_k, stoch_d, stoch_diff


def interpret_stoch(stoch_diff: float) -> str:
    if stoch_diff > 20:
        return "Güçlü Al"
    elif stoch_diff < -20:
        return "Güçlü Sat"
    elif stoch_diff > 0:
        return "Al"
    elif stoch_diff < 0:
        return "Sat"
    else:
        return "Nötr"