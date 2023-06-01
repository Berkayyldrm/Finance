from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException
from app.pivot_services.camarilla_service import calculate_camarilla_pivot_points, interpret_camarilla_pivot_points
from app.pivot_services.classic_service import calculate_classic_pivot_points, interpret_classic_pivot_points
from app.pivot_services.demark_service import calculate_demark_pivot_points, interpret_demark_pivot_points
from app.pivot_services.fibonacci_service import calculate_fibonacci_pivot_points, interpret_fibonacci_pivot_points
from app.pivot_services.woodie_service import calculate_woodie_pivot_points, interpret_woodie_pivot_points
from app.services.dataframe_service import get_data_as_dataframe, get_technical_data_as_dataframe
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/{symbol}/{date}/")
async def get_pivots(
    symbol: str,
    date: date,
    period: Optional[int] = 1
    ):

    available_dates = get_technical_data_as_dataframe(schema_name="general", table_name="availableDates")
    available_dates = available_dates["date"].tolist()

    def is_date_valid(input_date: date) -> bool:
        return input_date in available_dates

    if not is_date_valid(date):
        raise HTTPException(status_code=400, detail="Invalid date. Please provide a date from the available list.")
    
    data = get_data_as_dataframe(schema_name = "public", table_name=symbol)

    classic_support_levels, classic_resistance_levels, classic_pivot, current_price = calculate_classic_pivot_points(data=data, date=date, period=period)
    fibonacci_support_levels, fibonacci_resistance_levels, fibonacci_pivot, current_price = calculate_fibonacci_pivot_points(data=data, date=date, period=period)
    camarilla_support_levels, camarilla_resistance_levels, camarilla_pivot, current_price = calculate_camarilla_pivot_points(data=data, date=date, period=period)
    woodie_support_levels, woodie_resistance_levels, woodie_pivot, current_price = calculate_woodie_pivot_points(data=data, date=date, period=period)
    demark_support_levels, demark_resistance_levels, demark_pivot, current_price = calculate_demark_pivot_points(data=data, date=date, period=period)

    classic_sentiment = interpret_classic_pivot_points(current_price, classic_support_levels, classic_resistance_levels, classic_pivot)
    fibonacci_sentiment = interpret_fibonacci_pivot_points(current_price, fibonacci_support_levels, fibonacci_resistance_levels, fibonacci_pivot)
    camarilla_sentiment = interpret_camarilla_pivot_points(current_price, camarilla_support_levels, camarilla_resistance_levels, camarilla_pivot)
    woodie_sentiment = interpret_woodie_pivot_points(current_price, woodie_support_levels, woodie_resistance_levels, woodie_pivot)
    demark_sentiment = interpret_demark_pivot_points(current_price, demark_support_levels, demark_resistance_levels, demark_pivot)

    results = {
        "pivot_points": {
            "classic": {
                "support_levels": classic_support_levels,
                "resistance_levels": classic_resistance_levels,
                "pivot": classic_pivot,
                "current_price": current_price,
                "sentiment": classic_sentiment
            },
            "fibonacci": {
                "support_levels": fibonacci_support_levels,
                "resistance_levels": fibonacci_resistance_levels,
                "pivot": fibonacci_pivot,
                "current_price": current_price,
                "sentiment": fibonacci_sentiment
            },
            "camarilla": {
                "support_levels": camarilla_support_levels,
                "resistance_levels": camarilla_resistance_levels,
                "pivot": camarilla_pivot,
                "current_price": current_price,
                "sentiment": camarilla_sentiment
            },
            "woodie": {
                "support_levels": woodie_support_levels,
                "resistance_levels": woodie_resistance_levels,
                "pivot": woodie_pivot,
                "current_price": current_price,
                "sentiment": woodie_sentiment
            },
            "demark": {
                "support_levels": demark_support_levels,
                "resistance_levels": demark_resistance_levels,
                "pivot": demark_pivot,
                "current_price": current_price,
                "sentiment": demark_sentiment
            }
        }
        
    }
    return JSONResponse(results)