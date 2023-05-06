from database import Postgres
from app.models.data import BorsaData
from app.services.parse_service import parse_data
import configparser
from pandas import DataFrame
import os
import glob

# Config dosyasını oku
config = configparser.ConfigParser()
config.read("config.ini")

# Veritabanı bağlantı bilgilerini al
db_config = config["postgresql"]
database = db_config["database"]
user = db_config["user"]
password = db_config["password"]
host = db_config["host"]
port = db_config["port"]

def get_all_data(schema_name: str, table_name: str):
    postgres = Postgres(database=database, user=user, password=password, host=host, port=port)
    data = postgres.fetch_all(schema_name, table_name)
    postgres.close()

    borsa_data_list = []
    for row in data:
        parsed_data = parse_data(row)
        borsa_data = BorsaData(
            date=parsed_data.date,
            open=parsed_data.open,
            high=parsed_data.high,
            low=parsed_data.low,
            close=parsed_data.close,
            volume=parsed_data.volume,
            percentage=parsed_data.percentage,
            dividend=parsed_data.dividend,
            stock_split=parsed_data.stock_split
        )
        borsa_data_list.append(borsa_data)
    return borsa_data_list

def get_dataframe(table_name: str):
    postgres = Postgres(database=database, user=user, password=password, host=host, port=port)
    schema_name = "public"
    data = postgres.fetch_all(schema_name, table_name)
    postgres.close()

    df = DataFrame(data, columns=["date", "open", "high", "low", "close", "volume", "percentage"])
    return {table_name: df}

def create_data(input_data: str, table_name: str):
    parsed_data = parse_data(input_data)
    borsa_data = BorsaData(
        date=parsed_data[0],
        open=parsed_data[1],
        high=parsed_data[2],
        low=parsed_data[3],
        close=parsed_data[4],
        volume=parsed_data[5],
        percentage=parsed_data[6]
    )
    postgres = Postgres(database=database, user=user, password=password, host=host, port=port)
    
    query = f"INSERT INTO {table_name} (date, open, high, low, close, volume, percentage) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (borsa_data.date, borsa_data.open, borsa_data.high, borsa_data.low, borsa_data.close, borsa_data.volume, borsa_data.percentage)
    postgres.cur.execute(query, values)
    postgres.conn.commit()

    postgres.close()
    return borsa_data.dict()

def get_table_names_service():
    postgres = Postgres(database=database, user=user, password=password, host=host, port=port)
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    postgres.cur.execute(query)
    table_names = [row[0] for row in postgres.cur.fetchall()]
    postgres.close()
    return table_names

def get_service_list(folder_path: str):
    file_pattern = os.path.join(f"app/{folder_path}", "*.py")
    files = glob.glob(file_pattern)
    return [os.path.basename(file) for file in files if os.path.basename(file) != "__init__.py"]
