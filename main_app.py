from fastapi import FastAPI
import logging
from app.controllers import data_controller, technical_indicator_controller
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.include_router(data_controller.router, prefix="/data", tags=["data"])
app.include_router(technical_indicator_controller.router, prefix="/technical-indicators", tags=["technical-indicators"])
#app.include_router(data_router, prefix="/data")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)