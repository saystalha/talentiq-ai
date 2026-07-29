import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

_model = None

class EmbeddingService:
    """Service for computing text embeddings and semantic similarity."""

    @staticmethod
    def _load_model() -> SentenceTransformer:
        """Load the embedding model lazily as a singleton."""
        global _model
        if _model is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        return _model

    @staticmethod
    def get_embedding(text: str) -> list[float]:
        """Get the embedding vector for the given text."""
        if not text or not text.strip():
            return []
        
        model = EmbeddingService._load_model()
        embedding = model.encode(text)
        return embedding.tolist()

    @staticmethod
    def compute_similarity(text_a: str, text_b: str) -> float:
        """Compute cosine similarity between two texts."""
        if not text_a or not text_b or not text_a.strip() or not text_b.strip():
            return 0.0
            
        model = EmbeddingService._load_model()
        emb_a = model.encode([text_a])
        emb_b = model.encode([text_b])
        
        similarity = cosine_similarity(emb_a, emb_b)[0][0]
        return float(similarity)
