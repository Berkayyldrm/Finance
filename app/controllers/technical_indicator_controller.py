from fastapi import APIRouter, Depends
from app.services.dataframe_service import get_data_as_dataframe
from app.technical_indicator_services.atr_service import calculate_atr, interpret_atr
from app.technical_indicator_services.bull_bear_power_service import calculate_bull_bear_power, interpret_bull_bear_power
from app.technical_indicator_services.cci_service import calculate_cci, interpret_cci
from app.technical_indicator_services.highs_lows_service import calculate_hl, interpret_hl
from app.technical_indicator_services.roc_service import calculate_roc, interpret_roc
from app.technical_indicator_services.rsi_service import calculate_rsi, interpret_rsi
from app.technical_indicator_services.stoch_service import calculate_stoch, interpret_stoch
from app.technical_indicator_services.stochrsi_service import calculate_stochrsi, interpret_stochrsi
from app.technical_indicator_services.macd_service import calculate_macd, interpret_macd
from app.technical_indicator_services.adx_service import calculate_adx, interpret_adx
from app.technical_indicator_services.ultimate_oscillator_service import calculate_ultimate_oscillator, interpret_ultimate_oscillator
from app.technical_indicator_services.williams_r_service import calculate_williams_r, interpret_williams_r
from app.services.data_service import get_all_data
from app.models.data import BorsaData
from typing import List, Dict, Optional
from datetime import datetime, date
from fastapi.responses import JSONResponse
import numpy as np

router = APIRouter()

@router.get("/{symbol}/{date}/")
async def get_technical_indicators(
    symbol: str,
    date: date,
    rsi_period: Optional[int] = 14,
    stoch_k: Optional[int] = 9,
    stoch_d: Optional[int] = 6,
    stoch_smooth_k: Optional[int] = 3,
    stochrsi_period: Optional[int] = 14,
    stochrsi_rsi_period: Optional[int] = 14,
    stochrsi_k: Optional[int] = 3,
    stochrsi_d: Optional[int] = 3,
    macd_fast_period: Optional[int] = 12,
    macd_slow_period: Optional[int] = 26,
    macd_signal_period: Optional[int] = 9,
    adx_period: Optional[int] = 14,
    williams_r_period: Optional[int] = 14,
    cci_period: Optional[int] = 14,
    atr_period: Optional[int] = 14,
    hl_period: Optional[int] = 14,
    uo_short_period: Optional[int] = 7,
    uo_medium_period: Optional[int] = 14,
    uo_long_period: Optional[int] = 28,
    roc_period: Optional[int] = 14,
    bull_bear_power_period: Optional[int] = 13
    ):
    
    # Get all data for the symbol
    data = get_data_as_dataframe(schema_name="public", table_name=symbol)

    # Calculate all the indicator values
    rsi = calculate_rsi(data=data, date=date, period=rsi_period)
    stoch_k, stoch_d, stoch_diff = calculate_stoch(data=data, date=date, k=stoch_k, d=stoch_d, smooth_k=stoch_smooth_k)
    stochrsi_k, stochrsi_d = calculate_stochrsi(data=data, date=date, period=stochrsi_period, rsi_period=stochrsi_rsi_period, k=stochrsi_k, d=stochrsi_d)
    macd, macd_h, macd_s = calculate_macd(data=data, date=date, fast_period=macd_fast_period, slow_period=macd_slow_period, signal_period=macd_signal_period)
    adx, adx_dmp, adx_dmn = calculate_adx(data=data, date=date, period=adx_period)
    wr = calculate_williams_r(data=data, date=date, period=williams_r_period)
    cci = calculate_cci(data=data, date=date, period=cci_period)
    atr, atr_percentage = calculate_atr(data=data, date=date, period=atr_period)
    hl_ratio = calculate_hl(data=data, date=date, period=hl_period)
    uo = calculate_ultimate_oscillator(data=data, date=date, short_period=uo_short_period, medium_period=uo_medium_period, long_period=uo_long_period)
    roc = calculate_roc(data=data, date=date, period=roc_period)
    bull_power, bear_power = calculate_bull_bear_power(data=data, date=date, period=bull_bear_power_period)

    if adx_dmp > adx_dmn:
        adx_return = adx * 1
    else:
        adx_return = adx * -1

    rsi_sentiment = interpret_rsi(rsi)
    stoch_sentiment = interpret_stoch(stoch_diff)
    stochrsi_sentiment = interpret_stochrsi(stochrsi_k, stochrsi_d)
    macd_sentiment = interpret_macd(macd, macd_h, macd_s)
    adx_sentiment = interpret_adx(adx, adx_dmp, adx_dmn)
    wr_sentiment = interpret_williams_r(wr)
    cci_sentiment = interpret_cci(cci)
    atr_sentiment = interpret_atr(atr_percentage)
    hl_sentiment = interpret_hl(hl_ratio)
    uo_sentiment = interpret_ultimate_oscillator(uo)
    roc_sentiment = interpret_roc(roc)
    bull_bear_power_sentiment = interpret_bull_bear_power(bull_power, bear_power)
    
    results = {
        "technical_values":{
        "rsi": rsi,
        "stoch": {"stoch_k": stoch_k, "stoch_d": stoch_d, "stoch_diff": stoch_diff},
        "stochrsi": {"stochrsi_k": stochrsi_k, "stochrsi_d": stochrsi_d},
        "macd": {"macd": macd, "macdh": macd_h, "macds": macd_s},
        "adx":{"adx": adx, "adx_return": adx_return},
        "williams_r": wr,
        "cci": cci,
        "atr": {"atr": atr, "atr_percentage": atr_percentage},
        "hl_ratio": hl_ratio,
        "ultimate_oscillator": uo,
        "roc": roc,
        "bull_bear_power": {"bull_power": bull_power, "bear_power": bear_power}
        },
        "Sentiments":{
            "rsi": rsi_sentiment,
            "stoch": stoch_sentiment,
            "stochrsi": stochrsi_sentiment,
            "macd": macd_sentiment,
            "adx": adx_sentiment,
            "williams_r": wr_sentiment,
            "cci": cci_sentiment,
            "atr": atr_sentiment,
            "hl_ratio": hl_sentiment,
            "ultimate_oscillator": uo_sentiment,
            "roc": roc_sentiment,
            "bull_bear_power": bull_bear_power_sentiment
        }
        
    }

    return JSONResponse(results)
