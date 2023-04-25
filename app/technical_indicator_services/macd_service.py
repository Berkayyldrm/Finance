from datetime import datetime
import pandas as pd
import pandas_ta as ta

def calculate_macd(data: pd.DataFrame, date: str, fast_period: int, slow_period: int, signal_period: int) -> tuple:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    # Calculate the MACD value
    macd = ta.macd(filtered_data["close"], fast=fast_period, slow=slow_period, signal=signal_period)

    return macd['MACD_12_26_9'].iloc[-1], macd['MACDs_12_26_9'].iloc[-1], macd['MACDh_12_26_9'].iloc[-1]


def interpret_macd(macd: float, signal: float, histogram: float) -> str:
    """
    Interprets the given MACD, signal line, and histogram values and returns a message indicating the market sentiment.

    Args:
        macd (float): The MACD value.
        signal (float): The signal line value.
        histogram (float): The MACD histogram value.

    Returns:
        str: A message indicating the market sentiment.
    """
    if histogram > 0:
        if macd > signal:
            return "Strong Buy"
        else:
            return "Buy"
    elif histogram < 0:
        if macd < signal:
            return "Strong Sell"
        else:
            return "Sell"
    else:
        return "Neutral"