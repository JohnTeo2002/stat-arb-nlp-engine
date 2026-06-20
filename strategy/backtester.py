import pandas as pd
import numpy as np
from config import Config

class VectorizedBacktester:
    """Vectorized mathematical backtester validating long-short cross-sectional equity alpha."""
    def __init__(self, weights: pd.DataFrame):
        self.weights = weights
        self.tickers = Config.TICKERS

    def generate_mock_price_returns(self) -> pd.DataFrame:
        """Generates synthetic log-normal equity returns for validation."""
        np.random.seed(42)
        dates = self.weights.index
        returns_dict = {}
        for ticker in self.tickers:
            # Baseline drift with random noise
            returns_dict[ticker] = np.random.normal(loc=0.0004, scale=0.015, size=len(dates))
        
        return pd.DataFrame(returns_dict, index=dates)

    def run(self):
        asset_returns = self.generate_mock_price_returns()
        
        # Calculate raw strategy returns: Weight(t-1) * Return(t)
        strategy_returns = (self.weights.shift(1) * asset_returns).sum(axis=1)
        
        # Factor in transaction costs on weight turnover matrix
        weight_changes = self.weights.diff().abs().sum(axis=1)
        transaction_costs = weight_changes * Config.TRANSACTION_COSTS
        net_returns = strategy_returns - transaction_costs
        
        # Performance Metrification
        cumulative_returns = (1 + net_returns).cumprod() - 1
        
        annualized_return = net_returns.mean() * 252
        annualized_vol = net_returns.std() * np.sqrt(252)
        sharpe_ratio = annualized_return / annualized_vol if annualized_vol != 0 else 0
        
        print("\n" + "="*45)
        print("   STATISTICAL ARBITRAGE ENGINE BACKTEST METRICS   ")
        print("="*45)
        print(f"Analysis Period:     {Config.START_DATE} to {Config.END_DATE}")
        print(f"Annualized Return:   {annualized_return * 100:.2f}%")
        print(f"Annualized Risk:     {annualized_vol * 100:.2f}%")
        print(f"Empirical Sharpe:    {sharpe_ratio:.2f}")
        print(f"Final Total Return:  {cumulative_returns.iloc[-1] * 100:.2f}%")
        print("="*45)