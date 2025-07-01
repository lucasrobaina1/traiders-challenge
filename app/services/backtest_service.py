import logging
import pandas as pd
import numpy as np
from .indicator_service import calculate_sma

logger = logging.getLogger(__name__)

class TradingStrategy:
    """Encapsula la lógica para ejecutar un backtest de estrategia de trading."""

    def __init__(self, df: pd.DataFrame, initial_capital: float = 10000.0):
        self.df = df.copy()
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.shares = 0.0
        self.positions = 0  # 0 for flat, 1 for long
        self.portfolio_values = []
        self.num_operations = 0

    def backtest(self) -> dict:
        """Ejecuta el backtesting de la estrategia de cruce de medias móviles."""
        self.df['sma_5'] = calculate_sma(self.df['close'], 5)
        self.df['sma_20'] = calculate_sma(self.df['close'], 20)

        for i in range(len(self.df)):
            if pd.isna(self.df['sma_5'].iloc[i]) or pd.isna(self.df['sma_20'].iloc[i]):
                current_value = self.cash + self.shares * self.df['close'].iloc[i]
                self.portfolio_values.append(current_value)
                continue

            if self.df['sma_5'].iloc[i] > self.df['sma_20'].iloc[i] and self.positions == 0:
                self.shares = self.cash / self.df['close'].iloc[i]
                self.cash = 0
                self.positions = 1
                self.num_operations += 1
                logger.info(f"Executed BUY order at {self.df['close'].iloc[i]}")

            elif self.df['sma_5'].iloc[i] < self.df['sma_20'].iloc[i] and self.positions == 1:
                self.cash = self.shares * self.df['close'].iloc[i]
                self.shares = 0
                self.positions = 0
                self.num_operations += 1
                logger.info(f"Executed SELL order at {self.df['close'].iloc[i]}")

            current_value = self.cash + self.shares * self.df['close'].iloc[i]
            self.portfolio_values.append(current_value)

        # --- Calculate Performance Metrics ---
        final_value = self.portfolio_values[-1]
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100

        portfolio_series = pd.Series(self.portfolio_values).dropna()
        
        # Max Drawdown
        running_max = portfolio_series.cummax()
        drawdown = (running_max - portfolio_series) / running_max
        max_drawdown = drawdown.max() * 100

        # Sharpe Ratio (annualized)
        returns = portfolio_series.pct_change().dropna()
        if len(returns) > 1 and returns.std() != 0:
            # Assuming daily data, 252 trading days in a year
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
        else:
            sharpe_ratio = 0.0

        return {
            "total_return": round(total_return, 2),
            "num_operations": self.num_operations,
            "final_portfolio_value": round(final_value, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe_ratio, 2)
        }
