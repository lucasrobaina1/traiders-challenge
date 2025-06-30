# app/trading.py
import logging
from .functions import calculate_sma
import pandas as pd

logger = logging.getLogger(__name__)

class TradingStrategy:
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.shares = 0.0
        self.trade_count = 0
        self.peak_value = initial_capital
        self.max_drawdown = 0.0
        self.portfolio_history = [initial_capital]
        self.returns = None
        self.data = None

    def execute_strategy(self, data: pd.DataFrame) -> dict:
        self.data = data.copy()
        self.data['sma_5'] = calculate_sma(self.data['close'], 5)
        self.data['sma_20'] = calculate_sma(self.data['close'], 20)
        self.data.dropna(inplace=True)
        self.data.reset_index(drop=True, inplace=True)


        for i in range(1, len(self.data)):
            if (self.data['sma_5'].iloc[i] > self.data['sma_20'].iloc[i] and
                self.data['sma_5'].iloc[i-1] <= self.data['sma_20'].iloc[i-1] and
                self.shares == 0):
                self.shares = self.cash / self.data['close'].iloc[i]
                self.cash = 0.0
                self.trade_count += 1
                logger.info(
                    "Executed BUY order", 
                    extra={
                        "timestamp": str(self.data['timestamp'].iloc[i]),
                        "price": self.data['close'].iloc[i],
                        "shares_bought": self.shares
                    }
                )
            elif (self.data['sma_5'].iloc[i] < self.data['sma_20'].iloc[i] and
                  self.data['sma_5'].iloc[i-1] >= self.data['sma_20'].iloc[i-1] and
                  self.shares > 0):
                self.cash = self.shares * self.data['close'].iloc[i]
                shares_sold = self.shares
                self.shares = 0.0
                self.trade_count += 1
                logger.info(
                    "Executed SELL order",
                    extra={
                        "timestamp": str(self.data['timestamp'].iloc[i]),
                        "price": self.data['close'].iloc[i],
                        "shares_sold": shares_sold,
                        "profit": self.cash
                    }
                )

            portfolio_value = self.cash + self.shares * self.data['close'].iloc[i]
            self.portfolio_history.append(portfolio_value)
            self.peak_value = max(self.peak_value, portfolio_value)
            drawdown = (self.peak_value - portfolio_value) / self.peak_value
            self.max_drawdown = max(self.max_drawdown, drawdown)

        self.returns = self.data['close'].pct_change().dropna()

        return self.calculate_metrics()

    def calculate_metrics(self) -> dict:
        final_value = self.portfolio_history[-1]
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100

        sharpe_ratio = 0
        if self.returns.std() > 0:
            sharpe_ratio = (self.returns.mean() / self.returns.std()) * (252 ** 0.5)

        return {
            "total_return": round(total_return, 2),
            "num_operations": self.trade_count,
            "max_drawdown": round(self.max_drawdown * 100, 2),
            "sharpe_ratio": round(sharpe_ratio, 2)
        }
