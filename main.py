import asyncio
from config import Config
from pipeline.ingestion import DataIngestionStream
from pipeline.database import StructuredStorageLayer
from nlp.sentiment import SentimentAnalyzer
from nlp.topics import TopicModeler
from strategy.execution import AlphaSignalGenerator
from strategy.backtester import VectorizedBacktester

async def main():
    print("[Initialize] Initializing NLP Pipelines and Storage Drivers...")
    db = StructuredStorageLayer()
    sentiment_engine = SentimentAnalyzer()
    topic_engine = TopicModeler()
    
    # Warm up LDA
    corpus_warmup = [
        "regulatory scrutiny policy tech", "quarterly earnings beat guidance revenue", 
        "supply chain logistics disruption bottleneck", "cloud infrastructure computing scaling architecture"
    ]
    topic_engine.fit_warmup(corpus_warmup)
    
    streamer = DataIngestionStream()
    
    # Live asynchronous processing engine callback
    async def process_incoming_stream(payload):
        text = payload["text"]
        # Fast inference
        score = sentiment_engine.analyze_text(text)
        topic = topic_engine.extract_dominant_topic(text)
        
        # Save straight to structured analytical DB
        db.insert_signal(
            timestamp=payload["timestamp"],
            ticker=payload["ticker"],
            sentiment_score=score,
            dominant_topic=topic
        )

    print("[Stream] Ingesting low-latency textual data updates...")
    await streamer.stream_feed(callback=process_incoming_stream)
    
    print("[Compile] Converting unstructured cache layers to analytical space...")
    signal_df = db.to_dataframe()
    
    print("[Alpha Generation] Structuring predictive sentiment shift weight vectors...")
    weights = AlphaSignalGenerator.compute_signals(signal_df)
    
    print("[Backtest Engine] Executing historical vector strategy validation...")
    backtester = VectorizedBacktester(weights=weights)
    backtester.run()

if __name__ == "__main__":
    # Run structural event-driven async loop
    asyncio.run(main())