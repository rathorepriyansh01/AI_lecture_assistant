"""
=========================================================
AI Lecture Assistant
Embedding Service
Production Version
=========================================================

Responsibilities
----------------
1. Load transcript.json
2. Generate embeddings
3. Store vectors in ChromaDB
4. Update metadata
"""

import json
import logging
import time
from pathlib import Path

import chromadb
import torch

from sentence_transformers import SentenceTransformer

from backend.core.embedding_model import EmbeddingModel

from config.settings import (

    CHROMA_DB_PATH,

    EMBEDDING_MODEL,

    COLLECTION_NAME

)

from backend.utils.metadata_manager import MetadataManager

# ==========================================================
# CONFIGURATION
# ==========================================================

BATCH_SIZE = 64

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)


class EmbeddingService:

    def __init__(self):

        self.manager = MetadataManager()

        self.device = (

            "cuda"

            if torch.cuda.is_available()

            else "cpu"

        )

        # embedding model 

        self.model = EmbeddingModel()

        logger.info("=" * 70)

        logger.info("Loading Embedding Model...")

        

        logger.info("Embedding Model Loaded Successfully.")

        logger.info(f"Device : {self.device}")

        logger.info(f"Model  : {EMBEDDING_MODEL}")

        logger.info("=" * 70)

        from backend.core.chroma_client import ChromaClient

        self.chroma = ChromaClient()

        self.collection = self.chroma.collection
    
        # =====================================================
    # Load Lecture
    # =====================================================

    def load_lecture(

        self,

        lecture_id

    ):

        metadata = self.manager.load(

            lecture_id

        )

        transcript_path = Path(

            metadata["files"]["transcript_path"]

        )

        if not transcript_path.exists():

            raise FileNotFoundError(

                f"Transcript not found : {transcript_path}"

            )

        with open(

            transcript_path,

            "r",

            encoding="utf-8"

        ) as f:

            transcript = json.load(f)
        
        print("Transcript Keys :", transcript.keys())

        logger.info("=" * 70)

        logger.info(

            f"Lecture Loaded : {transcript['lecture_name']}"

        )

        logger.info(

            f"Total Chunks : {transcript['total_chunks']}"

        )

        logger.info("=" * 70)

        print("=" * 80)
        print("Transcript Keys:")
        print(transcript.keys())
        print("=" * 80)

        return metadata, transcript


    # =====================================================
    # Prepare Documents
    # =====================================================

    def prepare_documents(

        self,
        metadata,
        transcript

    ):
        print(id(metadata))
        print(id(transcript))
        print("=" * 80)
        print("TYPE :", type(transcript))
        print("IS DICT :", isinstance(transcript, dict))

        if isinstance(transcript, dict):
               print("KEYS :", transcript.keys())
               print("lecture_name exists :", "lecture_name" in transcript)
               print("VALUE :", transcript.get("lecture_name"))
        else:
                print(transcript)
                print("=" * 80)

        ids = []

        documents = []

        metadatas = []

        texts = []

        lecture_name = transcript["lecture_name"]

        lecture_id = metadata["lecture"]["lecture_id"]

        for chunk in transcript["chunks"]:
            
            ids.append(

            f"{transcript['lecture_id']}_{chunk['chunk_id']}"

            )

            documents.append(

                chunk["text"]

            )

            texts.append(

                chunk["text"]

            )

            lecture_id = metadata["lecture"]["lecture_id"]

            metadatas.append({

    "lecture_id": transcript["lecture_id"],

    "lecture_name": transcript["lecture_name"],

    "chunk_id": chunk["chunk_id"],

    "start": chunk["start"],

    "end": chunk["end"],

    "duration": chunk["duration"],

    "word_count": chunk["word_count"],

    "char_count": chunk["char_count"],

    "created_at": transcript["created_at"]

})

        logger.info(

            f"Prepared {len(documents)} documents."

        )

        return (

            ids,

            documents,

            metadatas,

            texts

        )
        # =====================================================
    # Generate Embeddings
    # =====================================================

    def generate_embeddings(

        self,

        texts

    ):

        logger.info("=" * 70)

        logger.info("Generating Embeddings...")

        logger.info("=" * 70)

        start_time = time.time()

        embeddings = []

        total_batches = (

            len(texts) + BATCH_SIZE - 1

        ) // BATCH_SIZE

        for batch_no, i in enumerate(

            range(0, len(texts), BATCH_SIZE),

            start=1

        ):

            batch = texts[

                i:i+BATCH_SIZE

            ]

            logger.info(

                f"Batch {batch_no}/{total_batches}"

            )

            batch_embeddings = self.model.encode(

            batch,

            convert_to_numpy=True,

            normalize_embeddings=True,

            batch_size=64

            )
            embeddings.extend(

                batch_embeddings.tolist()

            )

        total_time = round(

            time.time() - start_time,

            2

        )

        logger.info("=" * 70)

        logger.info(

            f"Embeddings Generated : {len(embeddings)}"

        )

        logger.info(

            f"Processing Time : {total_time} sec"

        )

        logger.info("=" * 70)

        if embeddings:
            logger.info(
            f"Embedding Dimension : {len(embeddings[0])}"
        )

        return embeddings
    
        # =====================================================
    # Store Embeddings in ChromaDB
    # =====================================================

    def store_in_chromadb(

        self,

        ids,

        documents,

        metadatas,

        embeddings

    ):

        logger.info("=" * 70)

        logger.info("Storing Embeddings in ChromaDB...")

        logger.info("=" * 70)

        start_time = time.time()

        total_batches = (

            len(ids) + BATCH_SIZE - 1

        ) // BATCH_SIZE

        for batch_no, i in enumerate(

            range(0, len(ids), BATCH_SIZE),

            start=1

        ):

            logger.info(

                f"Uploading Batch {batch_no}/{total_batches}"

            )

            self.chroma.upsert(

                ids=ids[i:i+BATCH_SIZE],

                documents=documents[i:i+BATCH_SIZE],

                metadatas=metadatas[i:i+BATCH_SIZE],

                embeddings=embeddings[i:i+BATCH_SIZE]

            )

        elapsed = round(

            time.time() - start_time,

            2

        )

        logger.info("=" * 70)

        logger.info("Upload Completed")

        logger.info(

            f"Documents in Collection : {self.chroma.count()}"

        )

        logger.info(

            f"Upload Time : {elapsed} sec"

        )

        logger.info("=" * 70)
        # =====================================================
    # Update Metadata
    # =====================================================

    def update_metadata(

        self,

        lecture_id,

        transcript,

        processing_time

    ):

        logger.info("=" * 70)

        logger.info("Updating Metadata...")

        logger.info("=" * 70)

        # ---------------------------------------------
        # Pipeline
        # ---------------------------------------------

        self.manager.update_pipeline(

            lecture_id,

            embedding_completed=True

        )

        # ---------------------------------------------
        # Statistics
        # ---------------------------------------------

        self.manager.update_statistics(

            lecture_id,

            embedded_chunks=transcript["total_chunks"]

        )

        # ---------------------------------------------
        # Models
        # ---------------------------------------------

        self.manager.update_models(

            lecture_id,

            embedding_model=EMBEDDING_MODEL

        )

        # ---------------------------------------------
        # Processing
        # ---------------------------------------------

        self.manager.update_processing(

            lecture_id,

            current_stage="Embedding Completed",

            processing_time=processing_time,

            last_error=""

        )

        logger.info(

            "Metadata Updated Successfully."

        )

        logger.info("=" * 70)

        return self.manager.load(

            lecture_id

        )
            # =====================================================
    # Process
    # =====================================================

    def process(

        self,

        lecture_id

    ):

        logger.info("=" * 70)

        logger.info(

            "Starting Embedding Pipeline..."

        )

        logger.info("=" * 70)

        overall_start = time.time()

        try:

            # -----------------------------------------
            # Load Lecture
            # -----------------------------------------

            metadata, transcript = self.load_lecture(

                lecture_id

            )

            # -----------------------------------------
            # Prepare Documents
            # -----------------------------------------

            ids, documents, metadatas, texts = self.prepare_documents(

                         metadata,

                        transcript

)

            

            # -----------------------------------------
            # Generate Embeddings
            # -----------------------------------------

            embeddings = self.generate_embeddings(

                texts

            )

            # -----------------------------------------
            # Store in ChromaDB
            # -----------------------------------------

            self.store_in_chromadb(

                ids,

                documents,

                metadatas,

                embeddings

            )

            processing_time = round(

                time.time() - overall_start,

                2

            )

            # -----------------------------------------
            # Update Metadata
            # -----------------------------------------

            self.update_metadata(

                lecture_id,

                transcript,

                processing_time

            )

            logger.info("=" * 70)

            logger.info(

                "EMBEDDING COMPLETED"

            )

            logger.info("=" * 70)

            logger.info(

                f"Lecture : {transcript['lecture_name']}"

            )

            logger.info(

                f"Chunks : {transcript['total_chunks']}"

            )

            logger.info(

                f"Collection Size : {self.chroma.count()}"

            )

            logger.info(

                f"Execution Time : {processing_time} sec"

            )

            logger.info("=" * 70)

            return self.manager.load(

                lecture_id

            )

        except Exception as e:

            logger.exception(

                "Embedding Failed."

            )

            self.manager.update_processing(

                lecture_id,

                current_stage="Embedding Failed",

                last_error=str(e)

            )
            

            raise