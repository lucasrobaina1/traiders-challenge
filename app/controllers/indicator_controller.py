import pandas as pd
from fastapi import Request, HTTPException
from app.services.indicator_service import calculate_sma, calculate_rsi, calculate_macd

def get_technical_indicators(request: Request) -> dict:    
    if not hasattr(request.app.state, 'data_df') or request.app.state.data_df is None:
        raise HTTPException(status_code=400, detail="No data uploaded yet")

    df = request.app.state.data_df.copy()
    
    sma_5 = calculate_sma(df['close'], 5)
    sma_20 = calculate_sma(df['close'], 20)
    rsi = calculate_rsi(df['close'], 14)
    macd_data = calculate_macd(df['close'])

    response = {
        "sma_5": sma_5.dropna().round(2).tolist(),
        "sma_20": sma_20.dropna().round(2).tolist(),
        "rsi": rsi.dropna().round(2).tolist(),
        "macd": {
            "line": macd_data["line"].dropna().round(2).tolist(),
            "signal": macd_data["signal"].dropna().round(2).tolist(),
            "histogram": macd_data["histogram"].dropna().round(2).tolist()
        }
    }
    
    return response
