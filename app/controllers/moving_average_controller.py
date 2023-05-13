from datetime import date
from fastapi import APIRouter, HTTPException
from app.moving_average_services.simple_moving_average_service import calculate_simple_moving_average, interpret_simple_moving_average
from app.moving_average_services.expo_moving_average_service import calculate_expo_moving_average, interpret_expo_moving_average
from app.services.dataframe_service import get_data_as_dataframe, get_technical_data_as_dataframe
from fastapi.responses import JSONResponse

router = APIRouter()

available_dates = get_technical_data_as_dataframe(schema_name="general", table_name="availableDates")
available_dates = available_dates["date"].tolist()

def is_date_valid(input_date: date) -> bool:
    return input_date in available_dates

@router.get("/simple/{symbol}/{date}/{period}")
async def calculate_simple_moving_average_value(symbol: str, date: date, period: int):
    if not is_date_valid(date):
        raise HTTPException(status_code=400, detail="Invalid date. Please provide a date from the available list.")
    
    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    # Get all data for the symbol
    ma, current_price = calculate_simple_moving_average(data, date, period)
    
    sentiment = interpret_simple_moving_average(ma, current_price)
    return JSONResponse({"ma": ma, "sentiment": sentiment})

@router.get("/expo/{symbol}/{date}/{period}")
async def calculate_expo_moving_average_value(symbol: str, date: date, period: int):
    if not is_date_valid(date):
        raise HTTPException(status_code=400, detail="Invalid date. Please provide a date from the available list.")

    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    # Get all data for the symbol
    ma, current_price = calculate_expo_moving_average(data, date, period)
    
    sentiment = interpret_expo_moving_average(ma, current_price)
    return JSONResponse({"ma": ma, "sentiment": sentiment})