from fastapi import APIRouter
from app.pivot_services.classic_service import calculate_classic_pivot_points, interpret_classic_pivot_points
from app.pivot_services.fibonacci_service import calculate_fibonacci_pivot_points, interpret_fibonacci_pivot_points
from app.services.dataframe_service import get_data_as_dataframe
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/classic/{symbol}/{date}")#?????????????
async def calculate_moving_average_value(symbol: str, date: str):

    data = get_data_as_dataframe(table_name=symbol)

    # Get all data for the symbol
    value = calculate_classic_pivot_points(data, date)
    current_price = value[-1]
    sentiment = interpret_classic_pivot_points(value, current_price)

    return JSONResponse({"value": value, "sentiment": sentiment})

@router.get("/fibonacci/{symbol}/{date}/{period}")
async def calculate_fibonacci_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(table_name=symbol)

    fibonacci_pivot_points = calculate_fibonacci_pivot_points(data, date, period)

    current_price = fibonacci_pivot_points[-1]
  
    sentiment = interpret_fibonacci_pivot_points(fibonacci_pivot_points, current_price)

    return {"fibonacci_pivot_points": fibonacci_pivot_points, "sentiment": sentiment}