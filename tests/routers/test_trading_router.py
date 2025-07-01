import pytest
from fastapi.testclient import TestClient
import os
import sys
from unittest.mock import patch
from fastapi import Request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app

MOCK_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'mocks', 'data.csv'))
MOCK_DATA_ERROR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'mocks', 'data_error.csv'))

@pytest.fixture(scope="function")
def test_app():
    with TestClient(app) as c:
        yield c

def test_upload_data_success(test_app):
    with open(MOCK_DATA_PATH, "rb") as f:
        response = test_app.post("/upload-data", files={"file": ("data.csv", f, "text/csv")})
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

def test_upload_data_fail_columns(test_app):
    with open(MOCK_DATA_ERROR_PATH, "rb") as f:
        response = test_app.post("/upload-data", files={"file": ("data_error.csv", f, "text/csv")})
    assert response.status_code == 400
    assert "Missing required columns" in response.json()["detail"]

@patch('app.controllers.indicator_controller.get_technical_indicators')
def test_get_indicators_router_success(mock_get_indicators, test_app):
    mock_result = {"sma_5": [1, 2, 3], "rsi": [4, 5, 6], "macd": {}}
    mock_get_indicators.return_value = mock_result
    
    response = test_app.get("/indicators")
    
    assert response.status_code == 200
    assert response.json() == mock_result
    
    mock_get_indicators.assert_called_once()
    request_arg = mock_get_indicators.call_args[0][0]
    assert isinstance(request_arg, Request)

@patch('app.controllers.backtest_controller.run_strategy_backtest')
def test_strategy_backtest_router_success(mock_run_backtest, test_app):
    mock_result = {"total_return": 10.5, "num_operations": 4}
    mock_run_backtest.return_value = mock_result
    
    response = test_app.get("/strategy-backtest?initial_capital=50000")
    
    assert response.status_code == 200
    assert response.json() == mock_result
    
    mock_run_backtest.assert_called_once()
    request_arg = mock_run_backtest.call_args[0][0]
    capital_arg = mock_run_backtest.call_args[0][1]
    assert isinstance(request_arg, Request)
    assert capital_arg == 50000.0
 
