import pandas as pd
import numpy as np

class AlphaSignalGenerator:
    """Converts raw semantic structural time-series data into actionable cross-sectional alphas."""
    @staticmethod
    def compute_signals(df: pd.DataFrame) -> pd.DataFrame:
        # Pivot into analytical structure: Rows = Timestamps, Columns = Tickers
        sentiment_pivot = df.pivot_table(index='timestamp', columns='ticker', values='sentiment_score').fillna(0)
        
        # Smooth out sentiment shifts via rolling Exponential Moving Average (EMA) to prevent high-turnover decay
        smoothed_sentiment = sentiment_pivot.ewm(span=5, min_periods=1).mean()
        
        # Generate cross-sectional ranking vector per day (Neutral Market Allocation)
        rank_df = smoothed_sentiment.rank(axis=1, method='average')
        mean_rank = rank_df.mean(axis=1)
        std_rank = rank_df.std(axis=1).replace(0, 1)
        
        # Standardized Long-Short Weight Matrix (Sum of weights = 0)
        weights = rank_df.sub(mean_rank, axis=0).div(std_rank, axis=0)
        # Normalize weights to constrain gross exposure to 100% long / 100% short
        weights = weights.div(weights.abs().sum(axis=1), axis=0).fillna(0)
        
        return weights