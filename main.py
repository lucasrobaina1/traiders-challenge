from fastapi import FastAPI
from app.routers.trading_router import router as trading_router
from app.config.logger import setup_logging

setup_logging()

app = FastAPI()

@app.on_event("startup")
def startup_event():
    app.state.data_df = None

app.include_router(trading_router)

