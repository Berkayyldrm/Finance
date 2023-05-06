from fastapi import APIRouter
from app.pivot_services.camarilla_service import calculate_camarilla_pivot_points, interpret_camarilla_pivot_points
from app.pivot_services.classic_service import calculate_classic_pivot_points, interpret_classic_pivot_points
from app.pivot_services.demark_service import calculate_demark_pivot_points, interpret_demark_pivot_points
from app.pivot_services.fibonacci_service import calculate_fibonacci_pivot_points, interpret_fibonacci_pivot_points
from app.pivot_services.woodie_service import calculate_woodie_pivot_points, interpret_woodie_pivot_points
from app.services.dataframe_service import get_data_as_dataframe
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/classic/{symbol}/{date}/{period}")
async def calculate_moving_average_value(symbol: str, date: str, period: int):

    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    support_levels, resistance_levels, pivot, current_price = calculate_classic_pivot_points(data, date, period)

    sentiment = interpret_classic_pivot_points(current_price, support_levels, resistance_levels, pivot)

    return JSONResponse({"pivot": pivot, "support_levels": support_levels, "resistance_levels": resistance_levels, "sentiment": sentiment})

@router.get("/fibonacci/{symbol}/{date}/{period}")
async def calculate_fibonacci_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    support_levels, resistance_levels, pivot, current_price = calculate_fibonacci_pivot_points(data, date, period)

    sentiment = interpret_fibonacci_pivot_points(current_price, support_levels, resistance_levels, pivot)

    return JSONResponse({"pivot": pivot, "support_levels": support_levels, "resistance_levels": resistance_levels, "sentiment": sentiment})

@router.get("/camarilla/{symbol}/{date}/{period}")
async def calculate_camarilla_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    support_levels, resistance_levels, pivot, current_price = calculate_camarilla_pivot_points(data, date, period)
  
    sentiment = interpret_camarilla_pivot_points(current_price, support_levels, resistance_levels, pivot)

    return JSONResponse({"pivot": pivot, "support_levels": support_levels, "resistance_levels": resistance_levels, "sentiment": sentiment})

@router.get("/woodie/{symbol}/{date}/{period}")
async def calculate_woodie_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    support_levels, resistance_levels, pivot, current_price = calculate_woodie_pivot_points(data, date, period)
  
    sentiment = interpret_woodie_pivot_points(current_price, support_levels, resistance_levels, pivot)

    return JSONResponse({"pivot": pivot, "support_levels": support_levels, "resistance_levels": resistance_levels, "sentiment": sentiment})

@router.get("/demark/{symbol}/{date}/{period}")
async def calculate_demark_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    support_levels, resistance_levels, pivot, current_price = calculate_demark_pivot_points(data, date, period)
  
    sentiment = interpret_demark_pivot_points(current_price, support_levels, resistance_levels, pivot)

    return JSONResponse({"pivot": pivot, "support_levels": support_levels, "resistance_levels": resistance_levels, "sentiment": sentiment})