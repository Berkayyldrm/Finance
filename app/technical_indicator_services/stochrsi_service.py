from typing import List
from datetime import date, timedelta, datetime
import numpy as np
from app.models.data import BorsaData
from app.technical_indicator_services.rsi_service import calculate_rsi
from app.technical_indicator_services.stoch_service import calculate_stoch


def calculate_stoch_rsi(filtered_data: List[BorsaData], date: date, period: int = 14, slow_period: int = 6, rsi_period: int = 14) -> float:
    """
    Calculates the Stochastic RSI (STOCHRSI) indicator for a given symbol and date.

    Args:
        filtered_data (List[BorsaData]): A list of BorsaData objects for the symbol to calculate the indicator for.
        date (date): The date to calculate the indicator for.
        period (int): The number of periods to use for the %K calculation. Defaults to 14.
        slow_period (int): The number of periods to use for the %D calculation. Defaults to 6.
        rsi_period (int): The number of periods to use for the RSI calculation. Defaults to 14.

    Returns:
        float: The STOCHRSI value.
    """
    date = datetime.strptime(date, "%Y-%m-%d").date()

    # Calculate the RSI values
    rsi_values = [calculate_rsi(filtered_data, str(d.date), period=rsi_period) for d in filtered_data if d.date <= date]

    # Calculate the Stochastic RSI values
    k_period = period * slow_period
    k_values = [(rsi_values[i] - min(rsi_values[i:k_period + i])) / (max(rsi_values[i:k_period + i]) - min(rsi_values[i:k_period + i])) * 100 for i in range(len(rsi_values) - k_period)]
    d_values = [np.mean(k_values[i:i+slow_period]) for i in range(len(k_values) - slow_period + 1)]

    return k_values[-1], d_values[-1]


def interpret_stoch_rsi(k_value: float, d_value: float) -> str:
    """
    Interprets the given STOCHRSI values and returns a message indicating the market sentiment.

    Args:
        k_value (float): The latest %K value.
        d_value (float): The latest %D value.

    Returns:
        str: A message indicating the market sentiment.
    """
    if k_value > d_value:
        return "Overbought"
    else:
        return "Oversold"