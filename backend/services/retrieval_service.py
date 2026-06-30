"""
=========================================================
AI Lecture Assistant
Retriever Service
Production Version
=========================================================
"""

import logging
import time

from backend.core.embedding_model import EmbeddingModel
from backend.core.chroma_client import ChromaClient

from config.settings import (
    TOP_K,
    SEARCH_K,
    SIMILARITY_THRESHOLD,
    MAX_CONTEXT_CHARS,
    EMBEDDING_MODEL,
    COLLECTION_NAME
)

# =====================================================
# LOGGER
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# Retriever Service
# =====================================================

class RetrieverService:

    def __init__(self):

        logger.info("=" * 70)
        logger.info("Initializing Retriever Service...")
        logger.info("=" * 70)

        self.embedding_model = EmbeddingModel()

        self.chroma = ChromaClient()

        self.collection = self.chroma.collection

        self.top_k = TOP_K

        self.search_k = SEARCH_K

        self.similarity_threshold = SIMILARITY_THRESHOLD

        self.max_context_chars = MAX_CONTEXT_CHARS

        logger.info("Retriever Ready")
        logger.info(f"Collection : {COLLECTION_NAME}")
        logger.info(f"Documents  : {self.collection.count()}")
        logger.info(f"Top K      : {self.top_k}")
        logger.info(f"Search K   : {self.search_k}")
        logger.info("=" * 70)

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

            "status": "healthy",

            "collection": COLLECTION_NAME,

            "documents": self.collection.count(),

            "embedding_model": EMBEDDING_MODEL,

            "top_k": self.top_k,

            "search_k": self.search_k,

            "threshold": self.similarity_threshold

        }
    # =====================================================
    # Generate Query Embedding
    # =====================================================

    def embed_query(

        self,

        question: str

    ):

        logger.info("=" * 70)

        logger.info("Generating Query Embedding...")

        logger.info("=" * 70)

        start = time.time()

        embedding = self.embedding_model.encode_query(

            question

        )

        elapsed = round(

            time.time() - start,

            3

        )

        logger.info(

            f"Embedding Generated ({elapsed} sec)"

        )

        logger.info(

            f"Dimension : {len(embedding)}"

        )

        logger.info("=" * 70)

        return embedding


    # =====================================================
    # Search ChromaDB
    # =====================================================

    def search(

        self,

        question,

        lecture_id=None

    ):

        logger.info("=" * 70)

        logger.info("Searching ChromaDB...")

        logger.info("=" * 70)

        query_embedding = self.embed_query(

            question

        )

        start = time.time()

        kwargs = {

            "query_embeddings": [

                query_embedding

            ],

            "n_results": self.search_k,

            "include": [

                "documents",

                "metadatas",

                "distances"

            ]

        }

        # ---------------------------------------------
        # Lecture Filter
        # ---------------------------------------------

        if lecture_id is not None:

            kwargs["where"] = {

                "lecture_id": lecture_id

            }

            logger.info(

                f"Lecture Filter : {lecture_id}"

            )

        results = self.collection.query(

            **kwargs

        )

        elapsed = round(

            time.time() - start,

            3

        )

        retrieved = len(

            results["documents"][0]

        )

        logger.info(

            f"Retrieved : {retrieved}"

        )

        logger.info(

            f"Search Time : {elapsed} sec"

        )

        logger.info("=" * 70)

        return results
    # =====================================================
    # Similarity Filter
    # =====================================================

    def filter_results(
        self,
        results
    ):

        logger.info("=" * 70)
        logger.info("Filtering Results...")
        logger.info("=" * 70)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        filtered = []

        for doc, meta, distance in zip(
            documents,
            metadatas,
            distances
        ):

            filtered.append({

            "text": doc,

            "metadata": meta,

            "distance": distance

            })

        logger.info(
            f"After Similarity Filter : {len(filtered)}"
        )

        return filtered
    # =====================================================
    # Remove Duplicate Chunks
    # =====================================================

    def remove_duplicates(
        self,
        chunks
    ):

        logger.info("Removing Duplicate Chunks...")

        unique = []

        seen = set()

        for chunk in chunks:

            text = chunk["text"].strip()

            if text not in seen:

                seen.add(text)

                unique.append(chunk)

        logger.info(
            f"After Duplicate Removal : {len(unique)}"
        )

        return unique
        # =====================================================
    # Sort By Distance
    # =====================================================

    def sort_results(
        self,
        chunks
    ):

        return sorted(

            chunks,

            key=lambda x: x["distance"]

        )
    # =====================================================
    # Keep Top K
    # =====================================================

    def keep_top_k(
        self,
        chunks
    ):

        return chunks[:self.top_k]
    # =====================================================
    # Build Context
    # =====================================================

    def build_context(
        self,
        chunks
    ):

        logger.info("=" * 70)
        logger.info("Building Context...")
        logger.info("=" * 70)

        context = ""

        current_size = 0

        for i, chunk in enumerate(chunks, start=1):

            section = f"""

    ==================== Chunk {i} ====================

    Lecture : {chunk["metadata"]["lecture_name"]}

    Chunk ID : {chunk["metadata"]["chunk_id"]}

    Timestamp : {chunk["metadata"]["start"]:.2f}s - {chunk["metadata"]["end"]:.2f}s

    ---------------------------------------------------

    {chunk["text"]}

    """

            if current_size + len(section) > self.max_context_chars:
                break

            context += section
            current_size += len(section)

        logger.info(
            f"Context Length : {len(context)} characters"
        )

        return context
    # =====================================================
    # Build Sources
    # =====================================================

    def build_sources(self, chunks):

        sources = []

        for chunk in chunks:

            meta = chunk["metadata"]

            sources.append({

                "lecture_id": meta.get(

                    "lecture_id",

                    "unknown"

                ),

                "lecture_name": meta.get(

                    "lecture_name",

                    "Unknown"

                ),

                "chunk_id": meta.get(

                    "chunk_id"

                ),

                "start": meta.get(

                    "start"

                ),

                "end": meta.get(

                    "end"

                ),

                "distance": round(

                    chunk["distance"],

                    4

                )

            })

        return sources
    # =====================================================
    # Build Statistics
    # =====================================================

    def build_statistics(
        self,
        chunks,
        context
    ):

        return {

            "retrieved_chunks": len(chunks),

            "context_length": len(context),

            "average_distance": round(

                sum(

                    c["distance"]

                    for c in chunks

                ) / max(len(chunks), 1),

                4

            )

        }
    # =====================================================
    # Build Retrieval Response
    # =====================================================

    def build_response(
        self,
        question,
        chunks
    ):

        context = self.build_context(
            chunks
        )

        sources = self.build_sources(
            chunks
        )

        statistics = self.build_statistics(
            chunks,
            context
        )

        return {

            "query": question,

            "context": context,

            "chunks": chunks,

            "sources": sources,

            "statistics": statistics,

            "count": len(chunks)

        }
    # =====================================================
    # Retrieve
    # =====================================================

    def retrieve(

        self,

        question,

        lecture_id=None

    ):

        logger.info("=" * 70)

        logger.info("Retriever Pipeline Started")

        logger.info("=" * 70)

        overall_start = time.time()

        try:

            # ---------------------------------------------
            # Search
            # ---------------------------------------------

            results = self.search(

                question,

                lecture_id

            )

            # ---------------------------------------------
            # Similarity Filter
            # ---------------------------------------------

            chunks = self.filter_results(

                results

            )

            # ---------------------------------------------
            # Remove Duplicates
            # ---------------------------------------------

            chunks = self.remove_duplicates(

                chunks

            )

            # ---------------------------------------------
            # Sort
            # ---------------------------------------------

            chunks = self.sort_results(

                chunks

            )

            # ---------------------------------------------
            # Keep Top K
            # ---------------------------------------------

            chunks = self.keep_top_k(

                chunks

            )

            # ---------------------------------------------
            # Build Response
            # ---------------------------------------------

            response = self.build_response(

                question,

                chunks

            )

            elapsed = round(

                time.time() - overall_start,

                3

            )

            response["statistics"]["execution_time"] = elapsed

            logger.info("=" * 70)

            logger.info("Retriever Finished")

            logger.info(

                f"Returned Chunks : {response['count']}"

            )

            logger.info(

                f"Execution Time : {elapsed} sec"

            )

            logger.info("=" * 70)

            return response

        except Exception as e:

            logger.exception(

                "Retriever Failed"

            )

            raise e
    