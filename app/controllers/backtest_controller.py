"""Controller to handle the business logic for backtesting."""

import pandas as pd
from fastapi import Request, HTTPException
from app.services.backtest_service import TradingStrategy

def run_strategy_backtest(request: Request, initial_capital: float) -> dict:
    """Orchestrates the execution of a trading strategy backtest."""

    if not hasattr(request.app.state, 'data_df') or request.app.state.data_df is None:
        raise HTTPException(status_code=400, detail="No data uploaded for backtesting.")

    df = request.app.state.data_df
    backtester = TradingStrategy(df, initial_capital)
    results = backtester.backtest()
    
    return results
