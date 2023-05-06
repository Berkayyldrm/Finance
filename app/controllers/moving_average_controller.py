from fastapi import APIRouter
from app.moving_average_services.simple_moving_average_service import calculate_simple_moving_average, interpret_simple_moving_average
from app.moving_average_services.expo_moving_average_service import calculate_expo_moving_average, interpret_expo_moving_average
from app.services.dataframe_service import get_data_as_dataframe
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/simple/{symbol}/{date}/{period}")
async def calculate_simple_moving_average_value(symbol: str, date: str, period: int):
    
    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    # Get all data for the symbol
    ma, current_price = calculate_simple_moving_average(data, date, period)
    
    sentiment = interpret_simple_moving_average(ma, current_price)
    return JSONResponse({"ma": ma, "sentiment": sentiment})

@router.get("/expo/{symbol}/{date}/{period}")
async def calculate_expo_moving_average_value(symbol: str, date: str, period: int):

    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    # Get all data for the symbol
    ma, current_price = calculate_expo_moving_average(data, date, period)
    
    sentiment = interpret_expo_moving_average(ma, current_price)
    return JSONResponse({"ma": ma, "sentiment": sentiment})