import pandas_ta as ta
import pandas as pd

def calculate_ultimate_oscillator(data: pd.DataFrame, fast_period: int = 7, mid_period: int = 14, slow_period: int = 28) -> float:
    true_range = ta.true_range(data["high"], data["low"], data["close"])
    avg_price = (data["high"] + data["low"] + data["close"]) / 3

    fast_avg = avg_price.rolling(fast_period).mean()
    mid_avg = avg_price.rolling(mid_period).mean()
    slow_avg = avg_price.rolling(slow_period).mean()

    fast_tr = true_range.rolling(fast_period).sum()
    mid_tr = true_range.rolling(mid_period).sum()
    slow_tr = true_range.rolling(slow_period).sum()

    uo = (4 * fast_avg / fast_tr) + (2 * mid_avg / mid_tr) + (slow_avg / slow_tr)
    uo = uo / (4 + 2 + 1)

    return uo.iloc[-1]

def interpret_ultimate_oscillator(oscillator_value: float) -> str:
    if oscillator_value > 70:
        return "Overbought"
    elif 50 < oscillator_value <= 70:
        return "Neutral/Bullish"
    elif 30 < oscillator_value <= 50:
        return "Neutral/Bearish"
    else:
        return "Oversold"