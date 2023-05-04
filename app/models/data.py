from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from datetime import date

class BorsaData(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    percentage: float
    dividend: float
    stock_split: float