from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.machine_learning_services.get_feature_service import get_feature_service
from app.machine_learning_services.stock_based_std_ml_service import calculate_stock_based_std_ml

from app.services.dataframe_service import get_technical_data_as_dataframe


router = APIRouter()

@router.get("/stock/std-ml/{symbol}")
async def calculate_stock_based_std_ml_value(symbol: str):
    data = get_technical_data_as_dataframe(schema_name="technical", table_name=symbol)
    data = get_feature_service(data)
    stock_std_ml = calculate_stock_based_std_ml(data=data)

    return JSONResponse({"result": stock_std_ml})