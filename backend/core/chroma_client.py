"""
=========================================================
AI Lecture Assistant
Shared Chroma Client
Production Version
=========================================================

Single ChromaDB client shared across all services.
"""

import logging

import chromadb

from config.settings import (

    CHROMA_DB_PATH,

    COLLECTION_NAME

)

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)


class ChromaClient:

    _instance = None

    _client = None

    _collection = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if ChromaClient._client is None:

            logger.info("=" * 70)

            logger.info("Connecting to ChromaDB...")

            logger.info("=" * 70)

            ChromaClient._client = chromadb.PersistentClient(

                path=CHROMA_DB_PATH

            )

            ChromaClient._collection = (

                ChromaClient._client.get_or_create_collection(

                    name=COLLECTION_NAME

                )

            )

            logger.info("Connected Successfully.")

            logger.info(

                f"Collection : {COLLECTION_NAME}"

            )

            logger.info("=" * 70)

    @property
    def client(self):

        return ChromaClient._client

    @property
    def collection(self):

        return ChromaClient._collection

    # =====================================================
    # Collection Info
    # =====================================================

    def count(self):

        return self.collection.count()

    # =====================================================
    # Add / Update
    # =====================================================

    def upsert(

        self,

        ids,

        documents,

        embeddings,

        metadatas

    ):

        self.collection.upsert(

            ids=ids,

            documents=documents,

            embeddings=embeddings,

            metadatas=metadatas

        )

    # =====================================================
    # Search
    # =====================================================

    def query(

        self,

        query_embedding,

        top_k=10

    ):

        return self.collection.query(

            query_embeddings=[

                query_embedding

            ],

            n_results=top_k,

            include=[

                "documents",

                "metadatas",

                "distances"

            ]

        )

    # =====================================================
    # Delete
    # =====================================================

    def delete(

        self,

        ids

    ):

        self.collection.delete(

            ids=ids

        )

    # =====================================================
    # Reset Collection
    # =====================================================

    def reset(self):

        self.client.delete_collection(

            COLLECTION_NAME

        )

        ChromaClient._collection = (

            self.client.create_collection(

                COLLECTION_NAME

            )

        )

        logger.info(

            "Collection Reset Successfully."

        )