from datetime import datetime
import pandas as pd
from typing import List, Tuple


def calculate_fibonacci_pivot_points(data: pd.DataFrame, date: str, period: int) -> Tuple[List[float], List[float], float]:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period)
    high, low = filtered_data['high'].max(), filtered_data['low'].min()
    print(filtered_data)
    range_diff = high - low
    ratios = [0.236, 0.382, 0.5, 0.618, 0.786]
    support_levels = []
    resistance_levels = []
    for ratio in ratios:
        retracement = range_diff * ratio
        support = low + retracement
        resistance = high - retracement

        support_levels.append(support)
        resistance_levels.append(resistance)

    current_price = filtered_data.iloc[0]['close']
    
    return support_levels, resistance_levels, current_price

def interpret_fibonacci_pivot_points(support_levels: List[float], resistance_levels: List[float], current_price: float) -> str:
    if current_price < support_levels[0]:
        return "Kapanış değeri en düşük destek seviyesinin altında, düşüş eğilimi bekleniyor."
    elif current_price > resistance_levels[-1]:
        return "Kapanış değeri en yüksek direnç seviyesinin üzerinde, yükseliş eğilimi bekleniyor."
    else:
        for i in range(len(support_levels) - 1):
            if support_levels[i] <= current_price <= support_levels[i + 1]:
                return f"Kapanış değeri Destek {i + 1} ve Destek {i + 2} arasında, yatay hareket bekleniyor."
        for i in range(len(resistance_levels) - 1):
            if resistance_levels[i] <= current_price <= resistance_levels[i + 1]:
                return f"Kapanış değeri Direnç {i + 1} ve Direnç {i + 2} arasında, yatay hareket bekleniyor."