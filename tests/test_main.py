import pytest
from fastapi.testclient import TestClient
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

# ·Test Setup

client = TestClient(app)

MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'mocks', 'data.csv')
MOCK_DATA_ERROR_PATH = os.path.join(os.path.dirname(__file__), '..', 'mocks', 'data_error.csv')

@pytest.fixture(scope="function")
def test_app():
    app.state.data_df = None
    with TestClient(app) as c:
        yield c

# Unit Tests

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

def test_get_indicators_no_data(test_app):
    response = test_app.get("/indicators")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data uploaded yet"}

def test_endpoints_after_upload(test_app):
    # Carga de datos
    with open(MOCK_DATA_PATH, "rb") as f:
        upload_response = test_app.post("/upload-data", files={"file": ("data.csv", f, "text/csv")})
    assert upload_response.status_code == 200

    # Test indicators
    indicators_response = test_app.get("/indicators")
    assert indicators_response.status_code == 200
    indicators_data = indicators_response.json()
    assert "sma_5" in indicators_data
    assert "rsi" in indicators_data
    assert isinstance(indicators_data["sma_5"], list)

    # Test backtest
    backtest_response = test_app.get("/strategy-backtest?initial_capital=50000")
    assert backtest_response.status_code == 200
    backtest_data = backtest_response.json()
    assert "total_return" in backtest_data
    assert "num_operations" in backtest_data 
