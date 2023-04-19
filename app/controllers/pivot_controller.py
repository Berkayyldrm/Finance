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

    data = get_data_as_dataframe(table_name=symbol)

    classic_pivot_points = calculate_classic_pivot_points(data, date, period)

    current_price = classic_pivot_points[-1]

    sentiment = interpret_classic_pivot_points(classic_pivot_points, current_price)

    return JSONResponse({"classic_pivot_points": classic_pivot_points, "sentiment": sentiment})

@router.get("/fibonacci/{symbol}/{date}/{period}")
async def calculate_fibonacci_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(table_name=symbol)

    support_levels, resistance_levels, current_price = calculate_fibonacci_pivot_points(data, date, period)

    sentiment = interpret_fibonacci_pivot_points(support_levels, resistance_levels, current_price)

    return JSONResponse({"support_levels": support_levels, "resistance_levels": resistance_levels, "sentiment": sentiment})

@router.get("/camarilla/{symbol}/{date}/{period}")
async def calculate_camarilla_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(table_name=symbol)

    camarilla_pivot_points = calculate_camarilla_pivot_points(data, date, period)

    current_price = camarilla_pivot_points[-1]
  
    sentiment = interpret_camarilla_pivot_points(camarilla_pivot_points, current_price)

    return {"camarilla_pivot_points": camarilla_pivot_points, "sentiment": sentiment}

@router.get("/woodie/{symbol}/{date}/{period}")
async def calculate_woodie_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(table_name=symbol)

    woodie_pivot_points = calculate_woodie_pivot_points(data, date, period)

    current_price = woodie_pivot_points[-1]
  
    sentiment = interpret_woodie_pivot_points(woodie_pivot_points, current_price)

    return {"woodie_pivot_points": woodie_pivot_points, "sentiment": sentiment}

@router.get("/demark/{symbol}/{date}/{period}")
async def calculate_demark_pivot_points_value(symbol: str, date: str, period: int):
    data = get_data_as_dataframe(table_name=symbol)

    demark_pivot_points = calculate_demark_pivot_points(data, date, period)

    current_price = demark_pivot_points[-1]
  
    sentiment = interpret_demark_pivot_points(demark_pivot_points, current_price)

    return {"demark_pivot_points": demark_pivot_points, "sentiment": sentiment}