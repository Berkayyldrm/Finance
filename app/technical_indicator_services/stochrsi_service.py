from datetime import datetime
import pandas as pd
import pandas_ta as ta

def calculate_stoch_rsi(data: pd.DataFrame, date: str, period: int, rsi_period: int, k: int, d: int) -> tuple:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    stochrsi = ta.stochrsi(close=filtered_data['close'], rsi_length=rsi_period, length=period, k=k, smooth_d=d)
    print(stochrsi)
    return stochrsi['STOCHRSIk_{}_{}_{}_{}'.format(rsi_period, period, k, d)].iloc[-1], stochrsi['STOCHRSId_{}_{}_{}_{}'.format(rsi_period, period, k, d)].iloc[-1]


def interpret_stoch_rsi(stochrsi_k: float, stochrsi_d: float) -> str:
    if stochrsi_k > 80 and stochrsi_d > 80:
        return "Overbought"
    elif stochrsi_k < 20 and stochrsi_d < 20:
        return "Oversold"
    elif stochrsi_k > stochrsi_d:
        return "Buy"
    elif stochrsi_k < stochrsi_d:
        return "Sell"
    else:
        return "Neutral"