import torch
from transformers import BertTokenizer, BertForSequenceClassification
from config import Config

class SentimentAnalyzer:
    """Transformer-based sentiment modeling optimized for financial context using FinBERT."""
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained(Config.FINBERT_MODEL)
        self.model = BertForSequenceClassification.from_pretrained(Config.FINBERT_MODEL)
        self.model.eval()
        self.labels = ['Neutral', 'Positive', 'Negative']

    def analyze_text(self, text: str) -> float:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=-1).squeeze().tolist()
        
        # Mapping logits to a continuous sentiment score: [-1.0, 1.0]
        # FinBERT labels mapping usually: 0 -> Neutral, 1 -> Positive, 2 -> Negative
        pos, neg, neu = predictions[1], predictions[2], predictions[0]
        sentiment_score = pos - neg
        return sentiment_score