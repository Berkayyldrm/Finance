from datetime import datetime
import pandas as pd
import pandas_ta as ta

def calculate_williams_r(data: pd.DataFrame, date: str, period: int = 14) -> float:
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    williams_r = ta.willr(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], length=period)

    return williams_r.iloc[-1]

def interpret_williams_r(williams_r: float) -> str:
    if williams_r < -80:
        return "Güçlü Sat"
    elif -80 <= williams_r < -50:
        return "Sat"
    elif -50 <= williams_r < -20:
        return "Al"
    elif -20 <= williams_r < 0:
        return "Aşırı Al"
    else:
        return "Nötr"