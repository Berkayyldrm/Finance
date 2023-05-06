from pandas import DataFrame
from app.services.data_service import get_all_data, get_all_technical_data
import pandas as pd

def get_data_as_dataframe(schema_name: str, table_name: str) -> DataFrame:
    data = get_all_data(schema_name, table_name)
    df = DataFrame([d.dict() for d in data])
    return df

def get_technical_data_as_dataframe(schema_name: str, table_name: str) -> DataFrame:
    data, column_names = get_all_technical_data(schema_name, table_name)
    df = pd.DataFrame(data)
    df.columns = column_names
    return df