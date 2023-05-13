from datetime import datetime, date
import pandas as pd
import pandas_ta as ta

def calculate_adx(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    adx = ta.adx(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], length=period)

    adx_ = adx[f"ADX_{period}"].iloc[-1]
    adx_dmp = adx[f"DMP_{period}"].iloc[-1]
    adx_dmn = adx[f"DMN_{period}"].iloc[-1]
    if adx_dmp > adx_dmn:
        adx_return = adx_ * 1
    else:
        adx_return = adx_ * -1 

    return adx_, adx_dmp, adx_dmn, adx_return

def calculate_adx_all(data: pd.DataFrame, date: date, period: int) -> float:

    filtered_data = data.loc[data['date'] <= date]

    adx = ta.adx(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], length=period)

    adx_ = adx[f"ADX_{period}"]
    adx_dmp = adx[f"DMP_{period}"]
    adx_dmn = adx[f"DMN_{period}"]
    
    def compute_adx_return(row):
        adx_, adx_dmp, adx_dmn = row
        if adx_dmp > adx_dmn:
            return adx_ * 1
        else:
            return adx_ * -1

    # Create a DataFrame from your Series
    adx_df = pd.DataFrame({f'{adx_}': adx_, f'{adx_dmp}': adx_dmp, f'{adx_dmn}': adx_dmn})
    # Apply the function to each row
    adx_return = adx_df.apply(compute_adx_return, axis=1)

    return adx_, adx_dmp, adx_dmn, adx_return

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