from fastapi import FastAPI
import logging
from datetime import datetime, timedelta
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import data_controller, machine_learning_controller, technical_indicator_controller, moving_average_controller, pivot_controller
from app.services.avaliable_date_service import available_date_service
from app.services.daily_data_service import daily_data_service
from app.services.technical_data_service import technical_data_service
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.include_router(data_controller.router, prefix="/data", tags=["data"])
app.include_router(technical_indicator_controller.router, prefix="/technical-indicator", tags=["technical-indicators"])
app.include_router(moving_average_controller.router, prefix="/moving-average", tags=["moving-average"])
app.include_router(pivot_controller.router, prefix="/pivot", tags=["pivot"])
app.include_router(machine_learning_controller.router, prefix="/machine-learning", tags=["machine-learning"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def my_task():
    while True:
        now = datetime.now()
        target_time = datetime(now.year, now.month, now.day, 23, 00)  # Her gün 23:00'de çalışacak

        if now > target_time:
            target_time += timedelta(days=1)  # Ertesi güne geçiş

        sleep_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(sleep_seconds)
        print("Daily Data Tasks Starting:", datetime.now())
        daily_data_service()
        print("Daily Data Task Executed:", datetime.now())
        available_date_service()
        print("Avaliable Date Task Executed:", datetime.now())
        technical_data_service()
        print("Technical Data Task Executed:", datetime.now())


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(my_task())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)