from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.data import BorsaData
from app.services.data_service import get_all_data, create_data
from typing import List
from pandas import DataFrame
from app.services.data_service import get_dataframe

router = APIRouter()

@router.get("/{table_name}", response_model=List[BorsaData])
def read_data(skip: int = 0, limit: int = 100, table_name: str = "aefes"):
    data = get_all_data(table_name=table_name)
    return data

@router.get("/dataframe/{table_name}")
async def read_dataframe(table_name: str, df: DataFrame = Depends(get_dataframe)):
    df = df[table_name]
    return df.to_dict(orient="records")

@router.post("/", response_model=BorsaData)
def add_data(data: BorsaData, table_name: str = None):
    return create_data(data.dict(), table_name=table_name)