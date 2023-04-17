from fastapi import APIRouter, Depends
from app.technical_indicator_services.rsi_service import calculate_rsi, interpret_rsi
from app.technical_indicator_services.stoch_service import calculate_stoch, interpret_stoch
from app.services.data_service import get_all_data
from app.models.data import BorsaData
from typing import List, Dict
from datetime import datetime
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/rsi/{symbol}/{date}")
async def calculate_rsi_value(symbol: str, date: str):
    # Get all data for the symbol
    data = get_all_data(table_name=symbol)

    # Filter the data for the specified date
    filtered_data = [d for d in data if datetime.combine(d.date, datetime.min.time()) <= datetime.fromisoformat(date)] # yyyy-mm-dd # verilen tarihten öncekiler geldi.

    # Calculate the RSI value
    rsi = calculate_rsi(filtered_data, date, period=14)

    # Interpret the RSI value
    sentiment = interpret_rsi(rsi)

    return JSONResponse({"rsi": rsi, "sentiment": sentiment})


@router.get("/stoch/{symbol}/{date}")
async def calculate_stoch_value(symbol: str,date: str, period: int = 9, slow_period: int = 6):
    # Get all data for the symbol
    data = get_all_data(table_name=symbol)

    filtered_data = [d for d in data if datetime.combine(d.date, datetime.min.time()) <= datetime.fromisoformat(date)] # yyyy-mm-dd # verilen tarihten öncekiler geldi.

    # Calculate the STOCH value
    k_value, d_value = calculate_stoch(filtered_data, date, period=period, slow_period=slow_period)

    sentiment = interpret_stoch(k_value, d_value)

    return JSONResponse({"stoch": d_value, "sentiment": sentiment})