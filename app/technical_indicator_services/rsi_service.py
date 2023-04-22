from datetime import datetime
import pandas as pd
import pandas_ta as ta



def calculate_rsi(data: pd.DataFrame, date: str, period: int = 14) -> float:
    
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    rsi = ta.rsi(filtered_data['close'], length=period)
    return rsi.iloc[-1]

def interpret_rsi(rsi_value: float) -> str:
    if rsi_value > 70:
        return "Güçlü Sat"
    elif rsi_value > 60:
        return "Sat"
    elif rsi_value < 30:
        return "Güçlü Al"
    elif rsi_value < 40:
        return "Al"
    else:
        return "Nötr"