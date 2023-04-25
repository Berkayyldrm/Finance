from datetime import datetime, timedelta
import pandas as pd
import pandas_ta as ta

def calculate_roc(data: pd.DataFrame, date: str, period: int) -> float:
    """
    7-14 days period

    Args:
    data (pd.DataFrame): A DataFrame containing prices and dates.
    date (str): The date to calculate ROC for in the format YYYY-MM-DD.
    period (int): The number of periods to use for the calculation. Defaults to 12.

    Returns:
    float: The ROC value.
    """
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]
    roc = ta.roc(filtered_data["close"], length=period)
    return roc.iloc[-1]

def interpret_roc(roc_value: float) -> str:
    if roc_value > 10:
        return "Güçlü Al"
    elif 5 < roc_value <= 10:
        return "Al"
    elif -5 <= roc_value <= 5:
        return "Nötr"
    elif -10 <= roc_value < -5:
        return "Sat"
    else:
        return "Güçlü Sat"