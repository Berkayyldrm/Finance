"""import pandas as pd
import pandas_ta as ta
from datetime import datetime

def calculate_cci(data: pd.DataFrame, date: str, period: int) -> float:
    # Convert date to datetime object
    date = datetime.fromisoformat(date)

    # Filter the data for the specified date and period
    start_date = (date - pd.DateOffset(days=period)).strftime("%Y-%m-%d")
    end_date = date.strftime("%Y-%m-%d")
    filtered_data = data.loc[(pd.to_datetime(data['date']) >= start_date) & (pd.to_datetime(data['date']) <= end_date)]
    print(filtered_data)

    # Calculate CCI value
    cci = ta.cci(high=filtered_data['high'], low=filtered_data['low'], close=filtered_data['close'], window=period)

    return cci[-1]


def interpret_cci(cci):
    if cci > 200:
        return "Aşırı Alım"
    elif 100 < cci <= 200:
        return "Güçlü Yükseliş Trendi"
    elif -100 <= cci <= 100:
        return "Normal Aralık"
    elif -200 <= cci < -100:
        return "Güçlü Düşüş Trendi"
    else:
        return "Aşırı Satış"""