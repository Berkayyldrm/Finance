from datetime import datetime, timedelta
import pandas as pd
import pandas_ta as ta

def calculate_bull_bear_power(data: pd.DataFrame, date: str, period: int) -> float:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]
    bull_power = filtered_data["high"] - ta.ema(filtered_data["close"], length=period)
    bear_power = filtered_data["low"] - ta.ema(filtered_data["close"], length=period)

    return bull_power.iloc[-1], bear_power.iloc[-1]


def interpret_bull_bear_power(bull_power: float, bear_power: float) -> str:
    if bull_power > 0 and bear_power < 0:
        return "Bullish"
    elif bull_power < 0 and bear_power > 0:
        return "Bearish"
    elif bull_power > 0 and bear_power > 0:
        return "Neutral to Bullish"
    elif bull_power < 0 and bear_power < 0:
        return "Neutral to Bearish"
    else:
        return "Neutral"