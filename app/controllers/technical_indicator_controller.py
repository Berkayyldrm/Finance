from fastapi import APIRouter, Depends
from app.services.dataframe_service import get_data_as_dataframe
from app.technical_indicator_services.atr_service import calculate_atr, interpret_atr
from app.technical_indicator_services.bull_bear_power_service import calculate_bull_bear_power, interpret_bull_bear_power
from app.technical_indicator_services.cci_service import calculate_cci, interpret_cci
from app.technical_indicator_services.highs_lows_service import calculate_hl, interpret_hl
from app.technical_indicator_services.roc_service import calculate_roc, interpret_roc
from app.technical_indicator_services.rsi_service import calculate_rsi, interpret_rsi
from app.technical_indicator_services.stoch_service import calculate_stoch, interpret_stoch
from app.technical_indicator_services.stochrsi_service import calculate_stoch_rsi, interpret_stoch_rsi
from app.technical_indicator_services.macd_service import calculate_macd, interpret_macd
from app.technical_indicator_services.adx_service import calculate_adx, interpret_adx
from app.technical_indicator_services.ultimate_oscillator_service import calculate_ultimate_oscillator, interpret_ultimate_oscillator
from app.technical_indicator_services.williams_r_service import calculate_williams_r, interpret_williams_r
from app.services.data_service import get_all_data
from app.models.data import BorsaData
from typing import List, Dict
from datetime import datetime
from fastapi.responses import JSONResponse
import numpy as np

router = APIRouter()

@router.get("/rsi/{symbol}/{date}/{period}")
async def calculate_rsi_value(symbol: str, date: str, period: int = 14):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate the RSI value
    rsi = calculate_rsi(data=data, date=date, period=period)

    # Interpret the RSI value
    sentiment = interpret_rsi(rsi)

    return JSONResponse({"rsi": rsi, "sentiment": sentiment})


@router.get("/stoch/{symbol}/{date}")
async def calculate_stoch_value(symbol: str, date: str, k: int = 9, d: int = 3, smooth_k: int = 6):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate the STOCH value
    stoch = calculate_stoch(data, date, k=k, d=d, smooth_k=smooth_k)

    sentiment = interpret_stoch(stoch[2])

    return JSONResponse({"stoch": {"stoch_k": stoch[0], "stoch_d": stoch[1], "stoch_diff": stoch[2]}, "sentiment": sentiment})


@router.get("/stochrsi/{symbol}/{date}")
async def calculate_stochrsi_value(symbol: str, date: str, period: int = 14, rsi_period: int = 14, k: int = 3, d: int = 3):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate the STOCHRSI value
    stochrsi = calculate_stoch_rsi(data, date, period=period, rsi_period=rsi_period, k=k, d=d)
    # Interpret the STOCHRSI value
    sentiment = interpret_stoch_rsi(stochrsi[0], stochrsi[1])

    return JSONResponse({"stochrsi": stochrsi, "sentiment": sentiment})

@router.get("/macd/{symbol}/{date}")
async def calculate_macd_value(symbol: str, date: str, fast_period: int, slow_period: int, signal_period: int):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate the MACD value
    macd = calculate_macd(data, date, fast_period=fast_period, slow_period=slow_period, signal_period=signal_period)
    # Interpret the MACD value
    sentiment = interpret_macd(macd[0], macd[1], macd[2])

    return JSONResponse({"macd": {"macd": macd[0], "macds":macd[1], "macdh":macd[2]}, "sentiment": sentiment})

@router.get("/adx/{symbol}/{date}")
async def calculate_adx_value(symbol: str, date: str, period: int = 14):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate the ADX value
    adx, dmp, dmn = calculate_adx(data, date, period=period)

    # Interpret the ADX value
    sentiment = interpret_adx(adx, dmp, dmn)

    if dmp > dmn:
        adx_return = adx * 1
    else:
        adx_return = adx * -1

    return JSONResponse({"adx": adx, "adx_return": adx_return, "sentiment": sentiment})


@router.get("/williams_r/{symbol}/{date}")
async def calculate_williams_r_value(symbol: str, date: str, period: int = 14):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate Williams %R value
    wr = calculate_williams_r(data, date, period=period)

    sentiment = interpret_williams_r(wr)

    return JSONResponse({"williams_r": wr, "sentiment": sentiment})

@router.get("/cci/{symbol}/{date}")
async def calculate_cci_value(symbol: str, date: str, period: int = 14):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate CCI value
    cci = calculate_cci(data, date, period=period)

    sentiment = interpret_cci(cci)

    return JSONResponse({"cci": cci, "sentiment": sentiment})

@router.get("/atr/{symbol}/{date}")
async def calculate_cci_value(symbol: str, date: str, period: int = 14):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate CCI value
    atr, percentage_atr = calculate_atr(data, date, period=period)

    sentiment = interpret_atr(percentage_atr)

    return JSONResponse({"atr": atr, "percentage_atr": percentage_atr, "sentiment": sentiment})

@router.get("/high_lows/{symbol}/{date}")
async def calculate_hl_value(symbol: str, date: str, period: int = 14):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate High/Low value
    ratio = calculate_hl(data, date, period=period)

    sentiment = interpret_hl(ratio)

    return JSONResponse({"ratio": ratio, "sentiment": sentiment})

@router.get("/ultimate_oscillator/{symbol}/{date}")
async def calculate_ultimate_oscillator_value(symbol: str, date: str, short_period: int = 7, medium_period: int = 14, long_period: int = 28):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol) 

    # Calculate the ultimate oscillator
    oscillator = calculate_ultimate_oscillator(data, date, short_period=short_period, medium_period=medium_period, long_period=long_period)

    # Interpret the oscillator value
    sentiment = interpret_ultimate_oscillator(oscillator)

    return JSONResponse({"oscillator": oscillator, "sentiment": sentiment})

@router.get("/roc/{symbol}/{date}/{period}")
async def calculate_roc_value(symbol: str, date: str, period: int = 14):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)

    # Calculate ROC value
    roc = calculate_roc(data, date, period=period)

    sentiment = interpret_roc(roc)

    return JSONResponse({"roc": roc, "sentiment": sentiment})

@router.get("/bull_bear_power/{symbol}/{date}") # X
async def calculate_bull_bear_power_value(symbol: str, date: str, period: int = 13):
    # Get all data for the symbol
    data = get_data_as_dataframe(table_name=symbol)
    # Calculate Bull/Bear Power value
    bull_power, bear_power = calculate_bull_bear_power(data, date, period)

    sentiment = interpret_bull_bear_power(bull_power, bear_power)

    return JSONResponse({"bull_power": bull_power, "bear_power": bear_power, "sentiment": sentiment})