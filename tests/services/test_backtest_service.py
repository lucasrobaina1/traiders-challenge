import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.backtest_service import TradingStrategy

@pytest.fixture
def sample_strategy_data():
    close_prices = np.concatenate([
        np.arange(100, 120, 1), 
        np.arange(120, 80, -1)  
    ])
    data = {'close': close_prices}
    df = pd.DataFrame(data)
    return df

def test_trading_strategy_initialization(sample_strategy_data):
    strategy = TradingStrategy(initial_capital=10000)
    assert strategy.initial_capital == 10000
    assert strategy.cash == 10000
    assert strategy.shares == 0.0
    assert strategy.positions == 0
    assert strategy.num_operations == 0
    assert len(strategy.portfolio_values) == 0

def test_trading_strategy_backtest(sample_strategy_data):
    strategy = TradingStrategy(initial_capital=10000)
    results = strategy.execute_strategy(sample_strategy_data)

    assert isinstance(results, dict)
    assert 'total_return' in results
    assert 'num_operations' in results
    assert 'final_portfolio_value' in results
    assert 'max_drawdown' in results
    assert 'sharpe_ratio' in results

    assert results['num_operations'] == 2
    assert isinstance(results['max_drawdown'], float)
    assert isinstance(results['sharpe_ratio'], float)
