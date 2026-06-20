import asyncio
import random
from datetime import datetime, timedelta
from config import Config

class DataIngestionStream:
    """Simulates a low-latency ingestion engine streaming unstructured textual data feeds."""
    def __init__(self):
        self.tickers = Config.TICKERS
        self.sample_texts = [
            "Executive transitions indicate massive structural tailwinds ahead for core cloud metrics.",
            "Supply chain bottlenecks present transitory headwinds to near-term margins.",
            "Regulatory scrutiny intensifies regarding next-generation AI model monentization architectures.",
            "Exceeded quarterly guidance driven by unprecedented enterprise-level SaaS adoption.",
            "Disruptive competitive pressures in hardware segmentation could margin squeeze market share."
        ]

    async def stream_feed(self, callback):
        """Asynchronously streams incoming text records to minimize signal decay."""
        current_date = datetime.strptime(Config.START_DATE, "%Y-%m-%d")
        end_date = datetime.strptime(Config.END_DATE, "%Y-%m-%d")
        
        while current_date <= end_date:
            # Simulate streaming bursts per day
            for ticker in self.tickers:
                payload = {
                    "timestamp": current_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "ticker": ticker,
                    "text": random.choice(self.sample_texts)
                }
                await callback(payload)
            
            # Step forward 1 trading day
            current_date += timedelta(days=1)
            await asyncio.sleep(0.001) # Yield control for event loop