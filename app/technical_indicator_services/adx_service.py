from typing import List
from app.models.data import BorsaData
from datetime import date, datetime, timedelta
import numpy as np

def calculate_adx(data: List[BorsaData], date: date, period: int = 14) -> float:
    """
    Calculates the Average Directional Index (ADX) of a given list of prices over a specified period.

    Args:
        data (List[BorsaData]): A list of prices.
        date (date): The date to calculate ADX for.
        period (int): The number of periods to use for the calculation. Defaults to 14.

    Returns:
        float: The ADX value.
    """
    date = datetime.strptime(date, "%Y-%m-%d").date()

    # Filter the prices for the specified period
    start_date = date - timedelta(days=period * 2)
    end_date = date - timedelta(days=1)

    filtered_data = [price for price in data if start_date <= price.date <= end_date]

    # Calculate the True Range (TR)
    true_ranges = []
    for i in range(1, len(filtered_data)):
        high_low = filtered_data[i].high - filtered_data[i].low
        high_pc = abs(filtered_data[i].high - filtered_data[i - 1].close)
        low_pc = abs(filtered_data[i].low - filtered_data[i - 1].close)
        true_ranges.append(max(high_low, high_pc, low_pc))
    atr = np.mean(true_ranges[:period])

    # Calculate the Positive Directional Movement (+DM) and Negative Directional Movement (-DM)
    positive_dms = []
    negative_dms = []
    for i in range(1, len(filtered_data)):
        high_diff = filtered_data[i].high - filtered_data[i - 1].high
        low_diff = filtered_data[i - 1].low - filtered_data[i].low
        if high_diff > low_diff and high_diff > 0:
            positive_dms.append(high_diff)
        else:
            positive_dms.append(0)
        if low_diff > high_diff and low_diff > 0:
            negative_dms.append(low_diff)
        else:
            negative_dms.append(0)
    pdm = np.mean(positive_dms[:period])
    ndm = np.mean(negative_dms[:period])

    # Calculate the Directional Movement Index (+DI and -DI)
    di_plus = 100 * (pdm / atr)
    di_minus = 100 * (ndm / atr)

    # Calculate the Directional Movement Index (DX)
    dx = 100 * (abs(di_plus - di_minus) / (di_plus + di_minus))

    # Calculate the Average Directional Index (ADX)
    dx_values = [dx]
    for i in range(period, len(filtered_data) - 1):
        dx = 100 * (abs(di_plus - di_minus) / (di_plus + di_minus))
        dx_values.append(dx)
        pdm = (pdm * (period - 1) + positive_dms[i]) / period
        ndm = (ndm * (period - 1) + negative_dms[i]) / period
        di_plus = 100 * (pdm / atr)
        di_minus = 100 * (ndm / atr)

    adx = np.mean(dx_values[-period:])

    return adx

def interpret_adx(adxi: float) -> str:
    if adxi > 25:
        return "Strong trend"
    else:
        return "Weak trend or ranging market"