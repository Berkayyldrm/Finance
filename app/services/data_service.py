from database import Postgres
from app.models.data import BorsaData
from app.services.parse_service import parse_data
import configparser
from pandas import DataFrame

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

def get_all_data(table_name: str):
    postgres = Postgres(database=database, user=user, password=password, host=host, port=port)
    data = postgres.fetch_all(table_name)
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
            percentage=parsed_data.percentage
        )
        borsa_data_list.append(borsa_data)
    return borsa_data_list

def get_dataframe(table_name: str):
    postgres = Postgres(database=database, user=user, password=password, host=host, port=port)
    data = postgres.fetch_all(table_name)
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