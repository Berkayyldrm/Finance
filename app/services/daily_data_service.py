from sqlalchemy import create_engine
import yfinance as yf
import configparser
import pandas as pd
import psycopg2
import sys
import sys
sys.path.insert(0, "c:/Users/Berkay/Desktop/Finance")

def daily_data_service():
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

    top_50_stock = ["AEFES", "AKBNK", "AKSA", "AKSEN", "ALARK", "ARCLK", "ASELS", "BERA", "BIMAS", "DOHOL",
                    "EGEEN", "EKGYO", "ENJSA", "ENKAI", "EREGL", "FROTO", "GARAN", "GESAN", "GUBRF",
                    "HALKB", "HEKTS", "ISCTR", "ISGYO", "KCHOL", "KONTR", "KORDS", "KOZAA", "KOZAA",
                    "KOZAL", "KRDMD", "MGROS", "ODAS", "OYAKC", "PETKM", "PGSUS", "SAHOL", "SASA",
                    "SISE", "SMRTG", "SOKM", "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TSKB",
                    "TTKOM", "TUPRS", "VAKBN", "VESTL", "YKBNK"]

    top_1_stock = ["AKSA"]

    def get_stock_data(symbol):
        suffix = ".IS"
        stock = yf.Ticker(symbol+suffix)
        return stock

    total_stocks = len(top_50_stock)

    for index, stock_symbol in enumerate(top_50_stock, start=1):
        stock = get_stock_data(stock_symbol)
        hist = stock.history(start="2021-01-04", end="2023-05-13")
        hist = hist.reset_index()
        hist = hist.sort_values(by='Date', ascending=False).reset_index(drop=True)

        hist['Date'] = pd.to_datetime(hist['Date']).dt.strftime('%Y.%m.%d')
        hist['Date'] = pd.to_datetime(hist['Date']).dt.date

        temp_df = hist['Close'].shift(-1)
        hist['Diff'] = hist['Close'] / temp_df
        hist['Diff'] = (1 - hist['Diff']) * -100
        hist = hist.iloc[:-1,:]
        hist.columns = ["date", "open", "high", "low", "close", "volume", "dividens", "stock splits", "diff"]
        hist.to_sql(stock_symbol, engine, schema="public", if_exists='replace', index=False)

        progress_percentage = (index / total_stocks) * 100
        sys.stdout.write("\rProgress: %.2f%%" % progress_percentage)
        sys.stdout.flush()