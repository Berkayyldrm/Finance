from datetime import datetime
import pandas as pd
import pickle 
import configparser

def calculate_general_ml(data: pd.DataFrame) -> float:
    config = configparser.ConfigParser()
    config.read("ml_model_features.ini", encoding="UTF-8")
    features = config.get("stock_based_std_ml", "features")
    features = [feature.strip() for feature in features.split(',')]
    data = data.iloc[-1:, :]
    model = pickle.load(open("./app/ml_models/general_ml.pkl", 'rb'))
    
    selected_data = data.loc[:, features]
    prediction = model.predict(selected_data)

    return float(prediction)
