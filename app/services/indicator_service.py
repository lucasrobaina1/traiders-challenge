import pandas as pd
import numpy as np

def validate_ohlc_data(df: pd.DataFrame) -> bool:
    """Valida estructura y calidad de datos OHLC"""
    required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_columns):
        return False
    if df[required_columns].isnull().values.any():
        return False
    return True

def calculate_sma(prices: pd.Series, window: int) -> pd.Series:
    """Calcula media móvil simple"""
    return prices.rolling(window=window).mean()

def calculate_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """Calcula RSI (Relative Strength Index)"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_indicators(df: pd.DataFrame) -> dict:
    """Calcula todos los indicadores técnicos y los devuelve en un diccionario."""
    return {
        "sma_5": calculate_sma(df['close'], 5),
        "sma_20": calculate_sma(df['close'], 20),
        "rsi": calculate_rsi(df['close']),
        "macd": calculate_macd(df['close']),
    }

def calculate_macd(prices: pd.Series) -> dict:
    """Calcula MACD line, signal line e histogram"""
    macd_line = prices.ewm(span=12).mean() - prices.ewm(span=26).mean()
    signal_line = macd_line.ewm(span=9).mean()
    histogram = macd_line - signal_line
    return {"line": macd_line, "signal": signal_line, "histogram": histogram}
