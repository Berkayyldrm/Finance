from datetime import datetime
import pandas as pd
import pandas_ta as ta

def calculate_adx(data: pd.DataFrame, date: str, period: int = 14) -> float:

    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    filtered_data = data.loc[data['date'] <= end_date]

    adx = ta.adx(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], length=period)
    print(adx)
    return adx[f"ADX_{period}"].iloc[-1], adx[f"DMP_{period}"].iloc[-1], adx[f"DMN_{period}"].iloc[-1]

def interpret_adx(adx: float, plus_di: float, minus_di: float) -> str:
    if adx > 25:
        if plus_di > minus_di:
            return "Güçlü Al"
        else:
            return "Güçlü Sat"
    else:
        if plus_di > minus_di:
            return "Al"
        elif plus_di < minus_di:
            return "Sat"
        else:
            return "Nötr"