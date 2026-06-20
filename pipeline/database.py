import pandas as pd

class StructuredStorageLayer:
    """Manages the structured time-series dataset post-NLP synthesis."""
    def __init__(self):
        self.storage = []

    def insert_signal(self, timestamp, ticker, sentiment_score, dominant_topic):
        self.storage.append({
            "timestamp": pd.to_datetime(timestamp),
            "ticker": ticker,
            "sentiment_score": sentiment_score,
            "dominant_topic": dominant_topic
        })

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.storage)
        if not df.empty:
            df.sort_values(by="timestamp", inplace=True)
        return df