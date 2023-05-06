from datetime import datetime
import pandas as pd

from app.services.dataframe_service import get_technical_data_as_dataframe

today = datetime.today().strftime("%Y-%m-%d")

top_50_stock = ["AEFES", "AKBNK", "AKSA", "AKSEN", "ALARK", "ARCLK", "ASELS", "BERA", "BIMAS", "DOHOL",
                "EGEEN", "EKGYO", "ENJSA", "ENKAI", "EREGL", "FROTO", "GARAN", "GESAN", "GUBRF",
                "HALKB", "HEKTS", "ISCTR", "ISGYO", "KCHOL", "KONTR", "KORDS", "KOZAA", "KOZAA",
                "KOZAL", "KRDMD", "MGROS", "ODAS", "OYAKC", "PETKM", "PGSUS", "SAHOL", "SASA",
                "SISE", "SMRTG", "SOKM", "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TSKB",
                "TTKOM", "TUPRS", "VAKBN", "VESTL", "YKBNK"]

top_1_stock = ["THYAO"]

for stock_symbol in top_1_stock:
    data = get_technical_data_as_dataframe(schema_name="technical", table_name=stock_symbol)

print(data)