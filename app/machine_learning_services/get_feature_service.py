import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def get_feature_service(data: pd.DataFrame):
    
    data = data.dropna()
    categoric_interpretation_columns = ["STOCH_Interpretation", "STOCHRSI_Interpretation", "MACD_Interpretation"]
    categoric_mapping = {
        "Güçlü Sat": 1,
        "Sat": 2,
        "Nötr": 3,
        "Al": 4,
        "Güçlü Al": 5
    }
    for column in categoric_interpretation_columns:
        data.loc[:, column] = data[column].map(categoric_mapping)
        data[column] = data[column].astype(int)
    return data

