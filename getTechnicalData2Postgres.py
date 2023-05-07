import configparser

from sqlalchemy import create_engine
from app.controllers.moving_average_controller import calculate_simple_moving_average_value
from app.moving_average_services.expo_moving_average_service import calculate_expo_moving_average_all, interpret_expo_moving_average_all
from app.moving_average_services.simple_moving_average_service import calculate_simple_moving_average, calculate_simple_moving_average_all, interpret_simple_moving_average_all
from app.pivot_services.camarilla_service import calculate_camarilla_pivot_points_all, interpret_camarilla_pivot_points_all
from app.pivot_services.classic_service import calculate_classic_pivot_points_all, interpret_classic_pivot_points_all
from app.pivot_services.demark_service import calculate_demark_pivot_points_all, interpret_demark_pivot_points_all
from app.pivot_services.fibonacci_service import calculate_fibonacci_pivot_points_all, interpret_fibonacci_pivot_points_all
from app.pivot_services.woodie_service import calculate_woodie_pivot_points_all, interpret_woodie_pivot_points_all
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

config = configparser.ConfigParser()
config.read("config.ini")

# Veritabanı bağlantı bilgilerini al
db_config = config["postgresql"]
database = db_config["database"]
user = db_config["user"]
password = db_config["password"]
host = db_config["host"]
port = db_config["port"]

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

today = datetime.today().strftime("%Y-%m-%d")

top_50_stock = ["AEFES", "AKBNK", "AKSA", "AKSEN", "ALARK", "ARCLK", "ASELS", "BERA", "BIMAS", "DOHOL",
                "EGEEN", "EKGYO", "ENJSA", "ENKAI", "EREGL", "FROTO", "GARAN", "GESAN", "GUBRF",
                "HALKB", "HEKTS", "ISCTR", "ISGYO", "KCHOL", "KONTR", "KORDS", "KOZAA", "KOZAA",
                "KOZAL", "KRDMD", "MGROS", "ODAS", "OYAKC", "PETKM", "PGSUS", "SAHOL", "SASA",
                "SISE", "SMRTG", "SOKM", "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TSKB",
                "TTKOM", "TUPRS", "VAKBN", "VESTL", "YKBNK"]

top_1_stock = ["THYAO"]

p = {

    "rsi_period": 14,

    "stoch_k": 9,
    "stoch_d": 6,
    "stoch_smooth_k": 3,

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

    "pivot_period": 1

}

for stock_symbol in top_1_stock:
    data = get_data_as_dataframe(schema_name="public", table_name=stock_symbol)
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
    hl_temp_df = hl_df[f"hl_ratio_{p['hl_period']}"].shift(p['hl_period']+1)
    hl_temp2_df = hl_df[f"hl_ratio_{p['hl_period']}"].iloc[-p['hl_period']+1:]
    hl_df = pd.concat([hl_temp_df, hl_temp2_df]).reset_index(drop=True)

    uo_df = pd.DataFrame(uo)

    roc_df = pd.DataFrame(roc)

    bullpower_df = pd.DataFrame(bull_power, columns=[f"Bull_power_{p['bullbear_period']}"])
    bearpower_df = pd.DataFrame(bear_power, columns=[f"Bear_power_{p['bullbear_period']}"])

    technical_df = pd.concat([data[["date"]], rsi_df, stoch_k_df, stoch_d_df, stoch_diff_df, stochrsi_k_df, stochrsi_d_df, macd_df, macd_h_df, macd_s_df,
               adx_df, adx_1_df, adx_2_df, willr_df, cci_df, atr_df, hl_df, uo_df, roc_df, bullpower_df, bearpower_df], axis=1)
    
    technical_df = technical_df.sort_values(by='date', ascending=False).reset_index(drop=True)

#####################################################################################################################################################################################

    ma_periods = [5, 10, 20, 50]

    ma_df = pd.DataFrame()

    for ma_period in ma_periods:
        sma, sma_current_price = calculate_simple_moving_average_all(data=data, date=today, period=ma_period)
        ma_df[f'SMA_{ma_period}'] = sma
        ma_df[f'SMA_interpretation_{ma_period}'] = interpret_simple_moving_average_all(ma_value=sma, current_price=sma_current_price)

        ema, ema_current_price = calculate_expo_moving_average_all(data=data, date=today, period=ma_period)
        ma_df[f'EMA_{ma_period}'] = ema
        ma_df[f'EMA_interpretation_{ma_period}'] = interpret_expo_moving_average_all(ma_value=ema, current_price=ema_current_price)
    
    ma_df = pd.concat([data["date"], ma_df], axis=1)
    ma_df = ma_df.sort_values(by='date', ascending=False).reset_index(drop=True)
    
#####################################################################################################################################################################################
    
    classic_pivot = calculate_classic_pivot_points_all(data=data, date=today, period=p["pivot_period"])
    classic_pivot_df = pd.DataFrame(classic_pivot, columns=["classic_support_levels", "classic_resistance_levels", "classic_pivot", "classic_current_price"])
    classic_pivot_interpretation = interpret_classic_pivot_points_all(classic_pivot_df["classic_current_price"], classic_pivot_df["classic_support_levels"], classic_pivot_df["classic_resistance_levels"], classic_pivot_df["classic_pivot"])
    classic_pivot_interpretation_df = pd.DataFrame(classic_pivot_interpretation, columns=["classic_pivot_interpretation"])

    fibonacci_pivot = calculate_fibonacci_pivot_points_all(data=data, date=today, period=p["pivot_period"])
    fibonacci_pivot_df = pd.DataFrame(fibonacci_pivot, columns=["fibonacci_support_levels", "fibonacci_resistance_levels", "fibonacci_pivot", "fibonacci_current_price"])
    fibonacci_pivot_interpretation = interpret_fibonacci_pivot_points_all(fibonacci_pivot_df["fibonacci_current_price"], fibonacci_pivot_df["fibonacci_support_levels"], fibonacci_pivot_df["fibonacci_resistance_levels"], fibonacci_pivot_df["fibonacci_pivot"])
    fibonacci_pivot_interpretation_df = pd.DataFrame(fibonacci_pivot_interpretation, columns=["fibonacci_pivot_interpretation"])
    
    camarilla_pivot = calculate_camarilla_pivot_points_all(data=data, date=today, period=p["pivot_period"])
    camarilla_pivot_df = pd.DataFrame(camarilla_pivot, columns=["camarilla_support_levels", "camarilla_resistance_levels", "camarilla_pivot", "camarilla_current_price"])
    camarilla_pivot_interpretation = interpret_camarilla_pivot_points_all(camarilla_pivot_df["camarilla_current_price"], camarilla_pivot_df["camarilla_support_levels"], camarilla_pivot_df["camarilla_resistance_levels"], camarilla_pivot_df["camarilla_pivot"])
    camarilla_pivot_interpretation_df = pd.DataFrame(camarilla_pivot_interpretation, columns=["camarilla_pivot_interpretation"])
    
    woodie_pivot = calculate_woodie_pivot_points_all(data=data, date=today, period=p["pivot_period"])
    woodie_pivot_df = pd.DataFrame(woodie_pivot, columns=["woodie_support_levels", "woodie_resistance_levels", "woodie_pivot", "woodie_current_price"])
    woodie_pivot_interpretation = interpret_woodie_pivot_points_all(woodie_pivot_df["woodie_current_price"], woodie_pivot_df["woodie_support_levels"], woodie_pivot_df["woodie_resistance_levels"], woodie_pivot_df["woodie_pivot"])
    woodie_pivot_interpretation_df = pd.DataFrame(woodie_pivot_interpretation, columns=["woodie_pivot_interpretation"])

    
    demark_pivot = calculate_demark_pivot_points_all(data=data, date=today, period=p["pivot_period"])
    demark_pivot_df = pd.DataFrame(demark_pivot, columns=["demark_support_levels", "demark_resistance_levels", "demark_pivot", "demark_current_price"])
    demark_pivot_interpretation = interpret_demark_pivot_points_all(demark_pivot_df["demark_current_price"], demark_pivot_df["demark_support_levels"], demark_pivot_df["demark_resistance_levels"], demark_pivot_df["demark_pivot"])
    demark_pivot_interpretation_df = pd.DataFrame(demark_pivot_interpretation, columns=["demark_pivot_interpretation"])

    pivot_df = pd.concat([data["date"], classic_pivot_interpretation_df, classic_pivot_df, fibonacci_pivot_interpretation_df, fibonacci_pivot_df,
                          camarilla_pivot_interpretation_df, camarilla_pivot_df, woodie_pivot_interpretation_df, woodie_pivot_df,
                          demark_pivot_interpretation_df, demark_pivot_df], axis=1)
    
    pivot_df = pivot_df.sort_values(by='date', ascending=False).reset_index(drop=True)

#################################################################################################################################################################################

    df = pd.concat([technical_df, ma_df, pivot_df], axis=1)
    df = df.loc[:,~df.columns.duplicated()].copy()
    df.to_sql(stock_symbol, engine, schema="technical", if_exists='replace', index=False)