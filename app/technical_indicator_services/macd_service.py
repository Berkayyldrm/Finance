from datetime import datetime
import pandas as pd
import pandas_ta as ta

def calculate_macd(data: pd.DataFrame, date: str, fast_period: int, slow_period: int, signal_period: int) -> float:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    macd = ta.macd(filtered_data["close"], fast=fast_period, slow=slow_period, signal=signal_period)
    print(macd)
    return macd[f'MACD_{fast_period}_{slow_period}_{signal_period}'].iloc[-1], macd[f'MACDh_{fast_period}_{slow_period}_{signal_period}'].iloc[-1], macd[f'MACDs_{fast_period}_{slow_period}_{signal_period}'].iloc[-1]

def calculate_macd_all(data: pd.DataFrame, date: str, fast_period: int, slow_period: int, signal_period: int) -> float:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    macd = ta.macd(filtered_data["close"], fast=fast_period, slow=slow_period, signal=signal_period)

    return macd[f'MACD_{fast_period}_{slow_period}_{signal_period}'], macd[f'MACDh_{fast_period}_{slow_period}_{signal_period}'], macd[f'MACDs_{fast_period}_{slow_period}_{signal_period}']


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
            return "Güçlü Al"
        else:
            return "Al"
    elif histogram < 0:
        if macd < signal:
            return "Güçlü Sat"
        else:
            return "Sat"
    else:
        return "Nötr"