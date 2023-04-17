from typing import List
from app.models.data import BorsaData
from datetime import datetime, timedelta
from app.services.data_service import get_all_data
from datetime import date

def calculate_macd(filtered_data: List[BorsaData], date: date, short_period: int = 12, long_period: int = 26, signal_period: int = 9) -> float:
    """
    Calculates the Moving Average Convergence/Divergence (MACD) value of a given list of prices over a specified period.

    Args:
        prices (List[float]): A list of prices.
        date (date): The date to calculate MACD for.
        short_period (int): The number of periods to use for the short-term moving average. Defaults to 12.
        long_period (int): The number of periods to use for the long-term moving average. Defaults to 26.
        signal_period (int): The number of periods to use for the signal line. Defaults to 9.

    Returns:
        float: The MACD value.
    """
    date = datetime.strptime(date, "%Y-%m-%d").date()

    # Filter the prices for the specified period
    start_date = date - timedelta(days=long_period + signal_period)
    end_date = date - timedelta(days=1)

    filtered_prices = [price for price in filtered_data if start_date <= price.date <= end_date]

    # Calculate the short-term and long-term moving averages
    short_term_ema = calculate_ema(filtered_prices, short_period)
    long_term_ema = calculate_ema(filtered_prices, long_period)

    # Calculate the MACD value
    macd = short_term_ema - long_term_ema

    # Calculate the signal line
    signal_line = calculate_ema(filtered_prices[-signal_period:], signal_period, start=macd)

    return macd - signal_line


def calculate_ema(prices: List[BorsaData], period: int, start: float = None) -> float:
    """
    Calculates the exponential moving average (EMA) of a given list of prices over a specified period.

    Args:
        prices (List[float]): A list of prices.
        period (int): The number of periods to use for the calculation.
        start (float): The starting value for the EMA calculation. Defaults to None.

    Returns:
        float: The EMA value.
    """
    if len(prices) == 0:
        return 0
    
    # Calculate the multiplier
    multiplier = 2 / (period + 1)
    
    # Initialize the EMA with the first price
    ema = prices[0].close
    
    # Calculate the EMA for the rest of the prices
    for i in range(1, len(prices)):
        close_price = prices[i].close
        ema = (close_price - ema) * multiplier + ema
    
    return ema


def interpret_macd(macd: float) -> str:
    """
    Interprets the given MACD value and returns a message indicating the market sentiment.

    Args:
        macd (float): The MACD value.

    Returns:
        str: A message indicating the market sentiment.
    """
    if macd > 0:
        return "Bullish"
    else:
        return "Bearish"