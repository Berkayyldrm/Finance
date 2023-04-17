import psycopg2
from psycopg2 import sql

class Postgres:
    def __init__(self, database, user, password, host, port):
        self.conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def fetch_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def close(self):
        self.conn.close()