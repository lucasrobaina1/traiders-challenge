import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Request
import pandas as pd

from app.services.indicator_service import validate_ohlc_data
from app.controllers import indicator_controller, backtest_controller

from app.config.openapi_config import (
    TAGS,
    UPLOAD_DATA_RESPONSES,
    GET_INDICATORS_RESPONSES,
    STRATEGY_BACKTEST_RESPONSES
)

logger = logging.getLogger(__name__)
router = APIRouter()

# EP 1 - Upload data
@router.post(
    "/upload-data", 
    tags=[TAGS["data"]], 
    responses=UPLOAD_DATA_RESPONSES
)
async def upload_data(request: Request, file: UploadFile = File(...)):
    """Upload OHLCV data from a CSV file

    Uploads a CSV file with market data. The file must contain the columns: 
    'timestamp', 'open', 'high', 'low', 'close', 'volume'.
    """
    df = pd.read_csv(file.file)
    if not validate_ohlc_data(df):
        logger.error("Data validation failed for uploaded file.")
        raise HTTPException(
            status_code=400,
            detail="Missing required columns (timestamp, open, high, low, close, volume)"
        )
    request.app.state.data_df = df
    logger.info(f"Data uploaded successfully.")
    return {"message": "Data uploaded successfully"}

# EP 2 - Indicators
@router.get(
    "/indicators", 
    tags=[TAGS["analysis"]], 
    responses=GET_INDICATORS_RESPONSES
)
async def get_indicators(request: Request):
    """Calculate technical indicators

    Calculates SMA (5, 20), RSI (14), and MACD on the uploaded data and returns them in JSON format.
    """
    return indicator_controller.get_technical_indicators(request)

# EP 3 - Backtesting 
@router.get(
    "/strategy-backtest", 
    tags=[TAGS["analysis"]], 
    responses=STRATEGY_BACKTEST_RESPONSES
)
async def strategy_backtest(
    request: Request, 
    initial_capital: float = Query(100000.0, gt=0, description="Specifies the initial capital.")):
    """Run a trading strategy backtest

    Simulates a moving average crossover strategy (SMA 5 vs SMA 20) and returns performance metrics.
    The initial capital is sent as an optional parameter with the request, default is 100000.
    """
    logger.info(f"Starting backtest with initial capital: {initial_capital}")
    results = backtest_controller.run_strategy_backtest(request, initial_capital)
    logger.info("Backtest finished.", extra={"results": results})
    return results
