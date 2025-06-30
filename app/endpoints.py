from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Request
import pandas as pd

from . import functions

router = APIRouter()

# EP 1 - Upload data
@router.post("/upload-data")
async def upload_data(request: Request, file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    if not functions.validate_ohlc_data(df):
        raise HTTPException(
            status_code=400,
            detail="Missing required columns (timestamp, open, high, low, close, volume)"
        )
    request.app.state.data_df = df
    return {"message": "Data uploaded successfully"}

# EP 2 - Indicators
@router.get("/indicators")
async def get_indicators(request: Request):
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
# El capital inicial se envía como parámetro opcional al hacer la solicitud, por defecto es 100000
@router.get("/strategy-backtest")
async def strategy_backtest(request: Request, initial_capital: float = Query(100000.0, gt=0)):
    print("initial_capital: {}".format(initial_capital))
    if not hasattr(request.app.state, 'data_df') or request.app.state.data_df is None:
        raise HTTPException(status_code=400, detail="No data uploaded for backtesting.")

    df = request.app.state.data_df.copy()
    
    # Calculo SMA 5 y 20
    df['sma_5'] = functions.calculate_sma(df['close'], 5)
    df['sma_20'] = functions.calculate_sma(df['close'], 20)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Para esta simulación empezamos desde cero con el capital inicial para comprar acciones:
    cash = initial_capital
    shares = 0.0
    trade_count = 0
    peak_value = initial_capital
    max_drawdown = 0.0
    portfolio_history = [initial_capital]

    for i in range(1, len(df)):
        # Compra:SMA5 cruza por encima de SMA20 y no tenemos acciones
        if df['sma_5'].iloc[i] > df['sma_20'].iloc[i] and df['sma_5'].iloc[i-1] <= df['sma_20'].iloc[i-1] and shares == 0:
            shares = cash / df['close'].iloc[i]
            cash = 0.0
            trade_count += 1
        # Venta: SMA5 cruza por debajo de SMA20 y tenemos acciones
        elif df['sma_5'].iloc[i] < df['sma_20'].iloc[i] and df['sma_5'].iloc[i-1] >= df['sma_20'].iloc[i-1] and shares > 0:
            cash = shares * df['close'].iloc[i]
            shares = 0.0
            trade_count += 1

        portfolio_value = cash + shares * df['close'].iloc[i]
        portfolio_history.append(portfolio_value)
        peak_value = max(peak_value, portfolio_value)
        drawdown = (peak_value - portfolio_value) / peak_value
        max_drawdown = max(max_drawdown, drawdown)

    final_portfolio_value = portfolio_history[-1]
    total_return = ((final_portfolio_value - initial_capital) / initial_capital) * 100

    returns = df['close'].pct_change().dropna()
    sharpe_ratio = 0
    if returns.std() > 0:
        sharpe_ratio = (returns.mean() / returns.std()) * (252 ** 0.5)

    return {
        "total_return": round(total_return, 2),
        "num_operations": trade_count,
        "max_drawdown": round(max_drawdown * 100, 2),
        "sharpe_ratio": round(sharpe_ratio, 2)
    }

# EP para verificar los datos cargados y debuggear
@router.get("/view-data")
async def view_data(request: Request):
    if request.app.state.data_df is None:
        return {"message": "No data uploaded yet"}
    return {
        "columns": list(request.app.state.data_df.columns),
        "rows": request.app.state.data_df.head(5).to_dict()
    }