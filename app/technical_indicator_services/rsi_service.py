from typing import List
from datetime import date, timedelta
import numpy as np
from datetime import datetime
from app.models.data import BorsaData


def calculate_rsi(filtered_data: List[BorsaData], date: date, period: int = 14) -> float:
    """
    Calculates the Relative Strength Index (RSI) of a given list of prices over a specified period.

    Args:
        prices (List[float]): A list of prices.
        date (date): The date to calculate RSI for.
        period (int): The number of periods to use for the calculation. Defaults to 14.

    Returns:
        float: The RSI value.
    """
    date = datetime.strptime(date, "%Y-%m-%d").date()

    # Filter the prices for the specified period
    start_date = date - timedelta(days=period)
    end_date = date - timedelta(days=1)

    filtered_prices = [price for price in filtered_data if start_date <= price.date <= end_date]

    # Calculate the differences between prices
    deltas = np.diff([price.close for price in filtered_prices])

    # Get the positive and negative price changes separately
    positive_deltas = deltas[deltas >= 0]
    negative_deltas = deltas[deltas < 0]

    # Calculate the average gain and loss over the specified period
    avg_gain = np.mean(positive_deltas[:period])
    avg_loss = np.abs(np.mean(negative_deltas[:period]))

    # Calculate the RSI value
    rs = avg_gain / avg_loss if avg_loss != 0 else np.inf
    rsi = 100 - (100 / (1 + rs))

    return rsi

def interpret_rsi(rsi: float) -> str:
    """
    Interprets the given RSI value and returns a message indicating the market sentiment.

    Args:
        rsi (float): The RSI value.

    Returns:
        str: A message indicating the market sentiment.
    """

    if rsi >= 70:
        return "Overbought"
    elif rsi <= 30:
        return "Oversold"
    else:
        return "Neutral"