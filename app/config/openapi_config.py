"""Centralized configuration for Swagger documentation."""

TAGS = {
    "data": "Data Management",
    "analysis": "Analysis and Backtesting"
}

# OpenAPI Response Models

UPLOAD_DATA_RESPONSES = {
    200: {
        "description": "Data uploaded and validated successfully.",
        "content": {
            "application/json": {
                "example": {"message": "Data uploaded successfully"}
            }
        }
    },
    400: {
        "description": "Validation error: The uploaded file is missing required columns.",
        "content": {
            "application/json": {
                "example": {"detail": "Missing required columns (timestamp, open, high, low, close, volume)"}
            }
        }
    }
}

GET_INDICATORS_RESPONSES = {
    200: {
        "description": "Technical indicators calculated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "sma_5": [102.0, 102.5],
                    "sma_20": [105.0, 105.2],
                    "rsi": [60.5, 62.1],
                    "macd": {
                        "line": [-0.5, -0.4],
                        "signal": [-0.55, -0.5],
                        "histogram": [0.05, 0.1]
                    }
                }
            }
        }
    },
    400: {
        "description": "No data has been uploaded yet.",
        "content": {
            "application/json": {
                "example": {"detail": "No data uploaded yet"}
            }
        }
    }
}

STRATEGY_BACKTEST_RESPONSES = {
    200: {
        "description": "Backtest completed successfully.",
        "content": {
            "application/json": {
                "example": {
                    "total_return": 5.25,
                    "num_operations": 4,
                    "final_portfolio_value": 10525.0,
                    "max_drawdown": 15.3,
                    "sharpe_ratio": 1.2
                }
            }
        }
    },
    400: {
        "description": "No data has been uploaded for backtesting.",
        "content": {
            "application/json": {
                "example": {"detail": "No data uploaded for backtesting."}
            }
        }
    }
}
