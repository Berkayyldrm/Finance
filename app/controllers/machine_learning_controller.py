from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.machine_learning_services.get_feature_service import get_feature_service
from app.machine_learning_services.general_ml import calculate_general_ml
from app.machine_learning_services.get_top_stock_service import get_top_stock_service

from app.services.dataframe_service import get_technical_data_as_dataframe


router = APIRouter()

top_50_stock = ["AEFES", "AKBNK", "AKSA", "AKSEN", "ALARK", "ARCLK", "ASELS", "BERA", "BIMAS", "DOHOL",
                "EGEEN", "EKGYO", "ENJSA", "ENKAI", "EREGL", "FROTO", "GARAN", "GESAN", "GUBRF",
                "HALKB", "HEKTS", "ISCTR", "ISGYO", "KCHOL", "KONTR", "KORDS", "KOZAA", "KOZAA",
                "KOZAL", "KRDMD", "MGROS", "ODAS", "OYAKC", "PETKM", "PGSUS", "SAHOL", "SASA",
                "SISE", "SMRTG", "SOKM", "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TSKB",
                "TTKOM", "TUPRS", "VAKBN", "VESTL", "YKBNK"]

@router.get("/stock/general-ml/{symbol}")
async def calculate_stock_based_std_ml_value(symbol: str):
    data = get_technical_data_as_dataframe(schema_name="technical", table_name=symbol)
    data = get_feature_service(data)
    stock_general_ml = calculate_general_ml(data=data)

    return JSONResponse({"result": stock_general_ml})

@router.get("/stock/top-10/general-ml/")
async def calculate_stock_based_std_ml_value():
    prediction_dict = {}
    for symbol in top_50_stock:
        data = get_technical_data_as_dataframe(schema_name="technical", table_name=symbol)
        data = get_feature_service(data)
        stock_general_ml = calculate_general_ml(data=data)
        prediction_dict[symbol] = stock_general_ml
    top_ten, worst_ten = get_top_stock_service(prediction_dict)


    return JSONResponse({"Top-10": top_ten, "Worst-10": worst_ten})