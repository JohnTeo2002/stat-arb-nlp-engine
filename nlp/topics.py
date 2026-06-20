from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from config import Config
import numpy as np

class TopicModeler:
    """Latent Dirichlet Allocation (LDA) Engine for unmasking latent thematic structure."""
    def __init__(self):
        self.vectorizer = CountVectorizer(stop_words='english')
        self.lda = LatentDirichletAllocation(n_components=Config.NUM_TOPICS, random_state=42)
        self._is_fitted = False

    def fit_warmup(self, sample_corpus):
        """Pre-fits the model on initial domain-specific corpus."""
        X = self.vectorizer.fit_transform(sample_corpus)
        self.lda.fit(X)
        self._is_fitted = True

    def extract_dominant_topic(self, text: str) -> int:
        if not self._is_fitted:
            return 0
        X = self.vectorizer.transform([text])
        topic_distribution = self.lda.transform(X)
        return int(np.argmax(topic_distribution))