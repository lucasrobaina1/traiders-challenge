import logging
import pandas as pd
import numpy as np
from typing import Dict, Any
from .indicator_service import calculate_sma

logger = logging.getLogger(__name__)

class TradingStrategy:
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.shares = 0.0
        self.positions = 0
        self.portfolio_values = []
        self.num_operations = 0
        self.df = None

    def execute_strategy(self, data: pd.DataFrame) -> Dict[str, Any]:
        self.df = data.copy()
        self.df['sma_5'] = calculate_sma(self.df['close'], 5)
        self.df['sma_20'] = calculate_sma(self.df['close'], 20)

        for i in range(len(self.df)):
            current_price = self.df['close'].iloc[i]
            if pd.isna(self.df['sma_5'].iloc[i]) or pd.isna(self.df['sma_20'].iloc[i]):
                self.portfolio_values.append(self.cash + self.shares * current_price)
                continue

            if self.df['sma_5'].iloc[i] > self.df['sma_20'].iloc[i] and self.positions == 0:
                self.shares = self.cash / current_price
                self.cash = 0
                self.positions = 1
                self.num_operations += 1
                logger.info(f"Executed BUY order at {current_price}")

            elif self.df['sma_5'].iloc[i] < self.df['sma_20'].iloc[i] and self.positions == 1:
                self.cash = self.shares * current_price
                self.shares = 0
                self.positions = 0
                self.num_operations += 1
                logger.info(f"Executed SELL order at {current_price}")

            self.portfolio_values.append(self.cash + self.shares * current_price)

        return self.calculate_metrics()

    def calculate_metrics(self) -> Dict[str, Any]:
        if not self.portfolio_values:
            return {
                "total_return": 0.0,
                "num_operations": 0,
                "final_portfolio_value": self.initial_capital,
                "max_drawdown": 0.0,
                "sharpe_ratio": 0.0
            }

        final_value = self.portfolio_values[-1]
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100

        portfolio_series = pd.Series(self.portfolio_values).dropna()
        
        running_max = portfolio_series.cummax()
        drawdown = (running_max - portfolio_series) / running_max
        max_drawdown = drawdown.max() * 100 if not drawdown.empty else 0.0

        returns = portfolio_series.pct_change().dropna()
        sharpe_ratio = 0.0
        if len(returns) > 1 and returns.std() != 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)

        return {
            "total_return": round(total_return, 2),
            "num_operations": self.num_operations,
            "final_portfolio_value": round(final_value, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe_ratio, 2)
        }
