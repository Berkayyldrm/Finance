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

    def fetch_all(self, schema_name, table_name):
        query = f'SELECT * FROM "{schema_name}"."{table_name}" ORDER BY "date" ASC'
        self.cur.execute(query)
        rows = self.cur.fetchall()

        return rows
    
    def fetch_all_with_column_names(self, schema_name, table_name):
        query = f'SELECT * FROM "{schema_name}"."{table_name}" ORDER BY "date" ASC'
        self.cur.execute(query)
        rows = self.cur.fetchall()

        query = f""" SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema_name}' AND table_name = '{table_name}';"""
        self.cur.execute(query)
        column_names = [row[0] for row in self.cur.fetchall()]

        return rows, column_names

    def close(self):
        self.conn.close()