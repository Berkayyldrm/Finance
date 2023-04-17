from fastapi import APIRouter, Depends
from app.technical_indicator_services.rsi_service import calculate_rsi, interpret_rsi
from app.technical_indicator_services.stoch_service import calculate_stoch, interpret_stoch
from app.technical_indicator_services.stochrsi_service import calculate_stoch_rsi, interpret_stoch_rsi
from app.technical_indicator_services.macd_service import calculate_macd, interpret_macd
from app.services.data_service import get_all_data
from app.models.data import BorsaData
from typing import List, Dict
from datetime import datetime
from fastapi.responses import JSONResponse
import numpy as np

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


@router.get("/stochrsi/{symbol}/{date}")
async def calculate_stochrsi_value(symbol: str, date: str, period: int = 14, slow_period: int = 6, rsi_period: int = 14):
    # Get all data for the symbol
    data = get_all_data(table_name=symbol)

    # Filter the data for the specified date
    filtered_data = [d for d in data if datetime.combine(d.date, datetime.min.time()) <= datetime.fromisoformat(date)]

    # Calculate the STOCHRSI value
    k_value, d_value = calculate_stoch_rsi(filtered_data, date, period=period, slow_period=slow_period, rsi_period=rsi_period)
    # Interpret the STOCHRSI value
    sentiment = interpret_stoch_rsi(k_value, d_value)

    return JSONResponse({"stochrsi": d_value, "sentiment": sentiment})

@router.get("/macd/{symbol}/{date}")
async def calculate_macd_value(symbol: str, date: str):
    # Get all data for the symbol
    data = get_all_data(table_name=symbol)

    # Filter the data for the specified date
    filtered_data = [d for d in data if datetime.combine(d.date, datetime.min.time()) <= datetime.fromisoformat(date)]

    # Calculate the MACD value
    macd = calculate_macd(filtered_data, date)

    # Interpret the MACD value
    sentiment = interpret_macd(macd)

    return JSONResponse({"macd": macd, "sentiment": sentiment})