import os

class Config:
    # NLP Models
    FINBERT_MODEL = "yiyanghkust/finbert-tone"
    NUM_TOPICS = 5  # LDA clusters
    
    # Backtest parameters
    START_DATE = "2023-01-01"
    END_DATE = "2026-01-01"
    INITIAL_CAPITAL = 10_000_000
    TRANSACTION_COSTS = 0.0005 # 5 bps
    
    # Simulated Assets
    TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]