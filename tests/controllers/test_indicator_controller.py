import pytest
import pandas as pd
from unittest.mock import Mock
from fastapi import HTTPException

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.controllers.indicator_controller import get_technical_indicators

@pytest.fixture
def sample_dataframe():
    """Crea un DataFrame de ejemplo para los tests."""
    data = {'close': [100, 101, 102, 103, 104, 105]}
    return pd.DataFrame(data)

def test_get_technical_indicators_success(sample_dataframe):
    """Verifica el cálculo exitoso de indicadores cuando hay datos."""
    request = Mock()
    request.app.state.data_df = sample_dataframe

    result = get_technical_indicators(request)

    assert isinstance(result, dict)
    assert "sma_5" in result
    assert "rsi" in result
    assert "macd" in result
    assert len(result["sma_5"]) > 0

def test_get_technical_indicators_no_data():
    """Verifica que se lanza una HTTPException cuando no hay datos."""
    request = Mock()
    request.app.state.data_df = None

    with pytest.raises(HTTPException) as excinfo:
        get_technical_indicators(request)
    
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "No data uploaded yet"
