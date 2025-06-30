from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd

app = FastAPI()

@app.on_event("startup")
def startup_event():
    app.state.data_df = None

@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(
            status_code=400,
            detail="Missing required columns"
        )

    app.state.data_df = df
    return {"message": "Data uploaded successfully"}
        
#EP para ver los datos cargados y debuggear
@app.get("/view-data")
async def view_data():
    if app.state.data_df is None:
        return {"message": "No data uploaded yet"}
    
    return {
        "columns": list(app.state.data_df.columns),
        "rows": app.state.data_df.head(5).to_dict() 
    }

#Endpoint 2 - Indicadores
@app.get("/indicators")
async def calculate_indicators():
    if app.state.data_df is None:
        return {"error": "No data uploaded yet"}
    
    df = app.state.data_df
    
    # Calculo SMA 5 y 20
    df['sma_5'] = df['close'].rolling(window=5).mean()
    df['sma_20'] = df['close'].rolling(window=20).mean()
    
    # Calculo RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Calculo MACD
    df['macd_line'] = df['close'].ewm(span=12).mean() - df['close'].ewm(span=26).mean()
    df['macd_signal'] = df['macd_line'].ewm(span=9).mean()
    df['macd_hist'] = df['macd_line'] - df['macd_signal']
    
    # Respuesta con valores acotados a 2 decimales
    return {
        "sma_5": df['sma_5'].dropna().round(2).tolist(),
        "sma_20": df['sma_20'].dropna().round(2).tolist(),
        "rsi": df['rsi'].dropna().round(2).tolist(),
        "macd": {
            "line": df['macd_line'].dropna().round(2).tolist(),
            "signal": df['macd_signal'].dropna().round(2).tolist(),
            "histogram": df['macd_hist'].dropna().round(2).tolist()
        }
    }