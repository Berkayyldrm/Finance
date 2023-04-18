from fastapi import APIRouter
from app.moving_average_services.moving_average_service import calculate_moving_average, interpret_moving_average
from app.services.dataframe_service import get_data_as_dataframe
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/{symbol}/{date}/{period}")
async def calculate_moving_average_value(symbol: str, date: str, period: int):

    data = get_data_as_dataframe(table_name=symbol)

    # Get all data for the symbol
    ma, current_price = calculate_moving_average(data, date, period)
    
    sentiment = interpret_moving_average(ma, current_price)
    return JSONResponse({"ma": ma, "sentiment": sentiment})