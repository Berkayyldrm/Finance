import pandas as pd

def get_feature_service(data: pd.DataFrame):
    interpretation_columns = [col for col in data.columns if 'interpretation' in col]
    for column in interpretation_columns:
        dummies = pd.get_dummies(data[column], prefix=column)
        data = pd.concat([data, dummies], axis=1)
        data.drop(column, axis=1, inplace=True)
    return data
