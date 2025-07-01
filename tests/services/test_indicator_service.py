import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.indicator_service import (
    calculate_sma,
    calculate_rsi,
    calculate_macd,
    calculate_indicators,
)

@pytest.fixture
def sample_dataframe():
    data = {
        'timestamp': pd.to_datetime(pd.date_range(start='2023-01-01', periods=30)),
        'open': np.random.uniform(98, 102, 30),
        'high': np.random.uniform(100, 105, 30),
        'low': np.random.uniform(95, 100, 30),
        'close': np.arange(100, 130),
        'volume': np.random.uniform(10000, 20000, 30),
    }
    return pd.DataFrame(data)

def test_calculate_sma(sample_dataframe):
    sma_5 = calculate_sma(sample_dataframe['close'], 5)
    assert isinstance(sma_5, pd.Series)
    assert sma_5.isnull().sum() == 4  
    assert round(sma_5.iloc[4], 2) == 102.0  

def test_calculate_rsi(sample_dataframe):
    rsi = calculate_rsi(sample_dataframe['close'], window=14)
    assert isinstance(rsi, pd.Series)
    assert rsi.isnull().sum() > 0
    assert rsi.iloc[-1] == 100.0  

def test_calculate_macd(sample_dataframe):
    macd = calculate_macd(sample_dataframe['close'])
    assert isinstance(macd, dict)
    assert 'line' in macd and 'signal' in macd and 'histogram' in macd
    assert isinstance(macd['line'], pd.Series)

def test_calculate_indicators(sample_dataframe):
    indicators = calculate_indicators(sample_dataframe)
    assert isinstance(indicators, dict)
    assert 'sma_5' in indicators
    assert 'sma_20' in indicators
    assert 'rsi' in indicators
    assert 'macd' in indicators
