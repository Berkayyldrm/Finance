from datetime import datetime, timedelta
import pandas as pd
import pandas_ta as ta

def calculate_roc(data: pd.DataFrame, date: str, period: int) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date].head(period+1)

    roc = ta.roc(filtered_data["close"], length=period)

    return roc.iloc[-1]

def interpret_roc(roc_value: float) -> str:
    if roc_value > 10:
        return "Yüksek olası alım fırsatı"
    elif 5 < roc_value <= 10:
        return "Olası alım fırsatı"
    elif -5 <= roc_value <= 5:
        return "Nötr bölge"
    elif -10 <= roc_value < -5:
        return "Olası satım fırsatı"
    else:
        return "Yüksek olası satım fırsatı"