from app.services.dataframe_service import get_data_as_dataframe
from datetime import datetime
import pandas as pd

from app.technical_indicator_services.adx_service import calculate_adx_all
from app.technical_indicator_services.atr_service import calculate_atr_all
from app.technical_indicator_services.bull_bear_power_service import calculate_bull_bear_power_all
from app.technical_indicator_services.cci_service import calculate_cci_all
from app.technical_indicator_services.highs_lows_service import calculate_hl_all
from app.technical_indicator_services.macd_service import calculate_macd_all
from app.technical_indicator_services.roc_service import calculate_roc_all
from app.technical_indicator_services.rsi_service import calculate_rsi_all
from app.technical_indicator_services.stoch_service import calculate_stoch_all
from app.technical_indicator_services.stochrsi_service import calculate_stoch_rsi_all
from app.technical_indicator_services.ultimate_oscillator_service import calculate_ultimate_oscillator_all
from app.technical_indicator_services.williams_r_service import calculate_williams_r_all

today = datetime.today().strftime("%Y-%m-%d")

top_50_stock = ["AEFES", "AKBNK", "AKSA", "AKSEN", "ALARK", "ARCLK", "ASELS", "BERA", "BIMAS", "DOHOL",
                "EGEEN", "EKGYO", "ENJSA", "ENKAI", "EREGL", "FROTO", "GARAN", "GESAN", "GUBRF",
                "HALKB", "HEKTS", "ISCTR", "ISGYO", "KCHOL", "KONTR", "KORDS", "KOZAA", "KOZAA",
                "KOZAL", "KRDMD", "MGROS", "ODAS", "OYAKC", "PETKM", "PGSUS", "SAHOL", "SASA",
                "SISE", "SMRTG", "SOKM", "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TSKB",
                "TTKOM", "TUPRS", "VAKBN", "VESTL", "YKBNK"]

top_1_stock = ["AKSA"]

p = {
    "rsi_period": 14,

    "stoch_k": 9,
    "stoch_d": 3,
    "stoch_smooth_k": 6,

    "stochrsi_period": 14,
    "stochrsi_rsi_period": 14,
    "stochrsi_k": 3,
    "stochrsi_d": 3,

    "macd_fast_period": 12,
    "macd_slow_period": 26,
    "macd_signal_period": 9,

    "adx_period": 14,

    "willr_period": 14,

    "cci_period": 14,

    "atr_period": 14,

    "hl_period": 14,

    "uo_short_period": 7,
    "uo_medium_period": 14,
    "uo_long_period": 28,

    "roc_period": 14,
    
    "bullbear_period": 13,

}

for symbol in top_1_stock:
    data = get_data_as_dataframe(table_name=symbol)
    
    rsi = calculate_rsi_all(data=data, date=today, period=p["rsi_period"])
    stoch_k, stoch_d, stoch_diff = calculate_stoch_all(data=data, date=today, k=p["stoch_k"], d=p["stoch_d"], smooth_k=p["stoch_smooth_k"])
    stochrsi_k, stochrsi_d = calculate_stoch_rsi_all(data=data, date=today, period=p["stochrsi_period"], rsi_period=p["stochrsi_rsi_period"], k=p["stochrsi_k"], d=p["stochrsi_d"])
    macd, macd_h, macd_s = calculate_macd_all(data=data, date=today, fast_period=p["macd_fast_period"], slow_period=p["macd_slow_period"], signal_period=p["macd_signal_period"])
    adx, adx_1, adx_2 = calculate_adx_all(data=data, date=today, period=p["adx_period"])
    willr = calculate_williams_r_all(data=data, date=today, period=p["willr_period"])
    cci = calculate_cci_all(data=data, date=today, period=p["cci_period"])
    atr = calculate_atr_all(data=data, date=today, period=p["atr_period"])
    hl = calculate_hl_all(data=data, date=today, period=p["hl_period"])
    uo = calculate_ultimate_oscillator_all(data=data, date=today, short_period=p["uo_short_period"], medium_period=p["uo_medium_period"], long_period=p["uo_long_period"])
    roc = calculate_roc_all(data=data, date=today, period=p["roc_period"])
    bull_power, bear_power = calculate_bull_bear_power_all(data=data, date=today, period=p["bullbear_period"])

    rsi_df = pd.DataFrame(rsi)

    stoch_k_df = pd.DataFrame(stoch_k)
    stoch_d_df = pd.DataFrame(stoch_d)
    stoch_diff_df = pd.DataFrame(stoch_diff, columns=["stoch_diff"])

    stochrsi_k_df = pd.DataFrame(stochrsi_k)
    stochrsi_d_df = pd.DataFrame(stochrsi_d)

    macd_df = pd.DataFrame(macd)
    macd_h_df = pd.DataFrame(macd_h)
    macd_s_df = pd.DataFrame(macd_s)

    adx_df = pd.DataFrame(adx)
    adx_1_df = pd.DataFrame(adx_1)
    adx_2_df = pd.DataFrame(adx_2)

    willr_df = pd.DataFrame(willr)

    cci_df = pd.DataFrame(cci)

    atr_df = pd.DataFrame(atr)

    hl_df = pd.DataFrame(hl, columns=[f"hl_ratio_{p['hl_period']}"])

    uo_df = pd.DataFrame(uo)

    roc_df = pd.DataFrame(roc)

    bullpower_df = pd.DataFrame(bull_power, columns=[f"Bull_power_{p['bullbear_period']}"])
    bearpower_df = pd.DataFrame(bear_power, columns=[f"Bear_power_{p['bullbear_period']}"])

    print(macd_h_df)