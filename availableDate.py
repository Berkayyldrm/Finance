from sqlalchemy import create_engine
import yfinance as yf
import configparser
import pandas as pd
import psycopg2
import sys

from app.services.dataframe_service import get_data_as_dataframe


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

example_stock_symbol = "THYAO"
schema_name = "availableDates"

data = get_data_as_dataframe(schema_name="public", table_name=example_stock_symbol)

df = pd.DataFrame(data.date, columns=["date"])

df.to_sql(schema_name, engine, schema="general", if_exists='replace', index=False)