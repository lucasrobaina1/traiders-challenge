import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Request
import pandas as pd

from . import functions
from .trading import TradingStrategy

logger = logging.getLogger(__name__)
router = APIRouter()

TAGS = {
    "data": "Data Management",
    "analysis": "Analysis and Strategies"
}

# EP 1 - Upload data
@router.post(
    "/upload-data", 
    tags=[TAGS["data"]], 
    responses={
        400: {
            "description": "The CSV file lacks required columns or contains null data.",
            "content": {
                "application/json": {
                    "example": {"detail": "Missing required columns (timestamp, open, high, low, close, volume)"}
                }
            }
        }
    }
)
async def upload_data(request: Request, file: UploadFile = File(...)):
    """Upload OHLCV data from a CSV file

    Uploads a CSV file with market data. The file must contain the columns: 
    'timestamp', 'open', 'high', 'low', 'close', 'volume'.
    """
    df = pd.read_csv(file.file)
    if not functions.validate_ohlc_data(df):
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
    responses={
        400: {
            "description": "No data has been uploaded yet.",
            "content": {
                "application/json": {
                    "example": {"detail": "No data uploaded yet"}
                }
            }
        }
    }
)
async def get_indicators(request: Request):
    """Calculate technical indicators

    Calculates SMA (5, 20), RSI (14), and MACD on the uploaded data and returns them in JSON format.
    """
    if request.app.state.data_df is None:
        raise HTTPException(status_code=400, detail="No data uploaded yet")
    
    df = request.app.state.data_df.copy() #Copia para no modificar el original

    # Realizo los calculos llamando a las funciones definidas en functions.py

    sma_5 = functions.calculate_sma(df['close'], 5)
    sma_20 = functions.calculate_sma(df['close'], 20)
    rsi = functions.calculate_rsi(df['close'])
    macd = functions.calculate_macd(df['close'])
    
    # Respuesta con valores acotados a 2 decimales
    return {
        "sma_5": sma_5.dropna().round(2).tolist(),
        "sma_20": sma_20.dropna().round(2).tolist(),
        "rsi": rsi.dropna().round(2).tolist(),
        "macd": {
            "line": macd["line"].dropna().round(2).tolist(),
            "signal": macd["signal"].dropna().round(2).tolist(),
            "histogram": macd["histogram"].dropna().round(2).tolist()
        }
    }

# EP 3 - Backtesting 
@router.get(
    "/strategy-backtest", 
    tags=[TAGS["analysis"]], 
    responses={
        400: {
            "description": "No data has been uploaded for backtesting.",
            "content": {
                "application/json": {
                    "example": {"detail": "No data uploaded for backtesting."}
                }
            }
        }
    }
)
async def strategy_backtest(
    request: Request, 
    initial_capital: float = Query(100000.0, gt=0, description="Initial capital for the simulation.")):
    """Run a trading strategy backtest

    Simulates a moving average crossover strategy (SMA 5 vs SMA 20) and returns performance metrics.
    The initial capital is sent as an optional parameter with the request, default is 100000.
    """
    if not hasattr(request.app.state, 'data_df') or request.app.state.data_df is None:
        logger.warning("Backtest attempt without data.")
        raise HTTPException(status_code=400, detail="No data uploaded for backtesting.")

    logger.info(f"Starting backtest with initial capital: {initial_capital}")
    backtester = TradingStrategy(initial_capital)
    results = backtester.execute_strategy(request.app.state.data_df)
    logger.info("Backtest finished.", extra={"results": results})
    return results
