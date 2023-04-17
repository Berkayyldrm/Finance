from pandas import DataFrame
from app.services.data_service import get_all_data

def get_data_as_dataframe(table_name: str) -> DataFrame:
    data = get_all_data(table_name)
    df = DataFrame([d.dict() for d in data])
    return df