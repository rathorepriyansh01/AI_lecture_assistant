"""
=========================================================
AI Lecture Assistant
Shared Embedding Model
Production Version
=========================================================

Loads the embedding model only once and shares it
across the entire application.
"""

import logging
import torch

from sentence_transformers import SentenceTransformer

from config.settings import EMBEDDING_MODEL

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class EmbeddingModel:

    _instance = None
    _model = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if EmbeddingModel._model is None:

            self.device = (
                "cuda"
                if torch.cuda.is_available()
                else "cpu"
            )

            logger.info("=" * 70)
            logger.info("Loading Shared Embedding Model...")
            logger.info("=" * 70)

            EmbeddingModel._model = SentenceTransformer(
                EMBEDDING_MODEL,
                device=self.device
            )

            logger.info("Embedding Model Loaded Successfully.")
            logger.info(f"Model  : {EMBEDDING_MODEL}")
            logger.info(f"Device : {self.device}")
            logger.info("=" * 70)

    @property
    def model(self):
        return EmbeddingModel._model

    # ------------------------------------------------------

    # =====================================================
# Encode
# =====================================================

    def encode(
        self,
        texts,
        **kwargs
    ):
        """
        Wrapper around SentenceTransformer.encode()

        This method is fully backward compatible with
        SentenceTransformer.encode().
        """

        kwargs.setdefault(
            "convert_to_numpy",
            True
        )

        kwargs.setdefault(
            "normalize_embeddings",
            True
        )

        kwargs.setdefault(
            "show_progress_bar",
            False
        )

        return self.model.encode(
            texts,
            **kwargs
        )

    # ------------------------------------------------------

    # =====================================================
    # Encode Query
    # =====================================================

    def encode_query(
        self,
        query
    ):

        return self.encode(query).tolist()

    # ------------------------------------------------------

    # =====================================================
    # Embedding Dimension
    # =====================================================

    def embedding_dimension(self):

        return len(
            self.encode("Hello")
        )