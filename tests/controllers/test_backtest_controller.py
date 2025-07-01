import pytest
import pandas as pd
from unittest.mock import Mock
from fastapi import HTTPException

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.controllers.backtest_controller import run_strategy_backtest

@pytest.fixture
def sample_dataframe():
    data = {'close': [100, 101, 102, 103, 104, 105, 104, 103, 102, 101, 100]}
    return pd.DataFrame(data)

def test_run_strategy_backtest_success(sample_dataframe):
    request = Mock()
    request.app.state.data_df = sample_dataframe
    initial_capital = 10000.0

    result = run_strategy_backtest(request, initial_capital)

    assert isinstance(result, dict)
    assert "total_return" in result
    assert "num_operations" in result
    assert "max_drawdown" in result
    assert "sharpe_ratio" in result

def test_run_strategy_backtest_no_data():
    request = Mock()
    request.app.state.data_df = None
    initial_capital = 10000.0

    with pytest.raises(HTTPException) as excinfo:
        run_strategy_backtest(request, initial_capital)
    
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "No data uploaded for backtesting."
