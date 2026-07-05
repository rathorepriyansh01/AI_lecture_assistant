"""
=========================================================
AI Lecture Assistant
Base AI Service
=========================================================
"""

import json
import time
import logging
from pathlib import Path
from abc import ABC
from config.settings import MAX_CONTEXT_CHARS

from backend.core.llm import LLMManager
from backend.core.prompt_manager import PromptManager

from backend.utils.cache_manager import CacheManager
from backend.utils.metadata_manager import MetadataManager
from backend.services.audio_service import AudioService
from backend.services.transcription_service import TranscriptionService
from backend.services.embedding_service import EmbeddingService


logger = logging.getLogger(__name__)


class BaseAIService(ABC):

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.data_root = self.project_root / "data"

        self.lecture_root = self.data_root / "lectures"

        self.llm = LLMManager()

        self.prompt_manager = PromptManager()

        self.cache = CacheManager()

        self.manager = MetadataManager()

        self.audio_service = AudioService()

        self.transcription_service = TranscriptionService()

        self.embedding_service = EmbeddingService()

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

            "status": "healthy",

            "llm": self.llm.health_check()

        }

    # =====================================================
    # Lecture Directory
    # =====================================================

    def get_lecture_directory(
        self,
        lecture_id
    ):

        return self.lecture_root / lecture_id

    # =====================================================
    # Load Transcript
    # =====================================================

    def load_transcript(
        self,
        lecture_id
    ):

        transcript_path = (

            self.get_lecture_directory(
                lecture_id
            )

            / "transcript.json"

        )

        logger.info(

            f"Loading Transcript : {transcript_path}"

        )

        with open(

            transcript_path,

            "r",

            encoding="utf-8"

        ) as f:

            transcript = json.load(f)

        return transcript

    # =====================================================
    # Load Metadata
    # =====================================================

    def load_metadata(
        self,
        lecture_id
    ):

        return self.manager.load(

            lecture_id

        )

    # =====================================================
    # Save Metadata
    # =====================================================

    def save_metadata(
        self,
        lecture_id,
        metadata
    ):

        self.manager.save(

            lecture_id,

            metadata

        )

    # =====================================================
    # Build Context
    # =====================================================

    def build_context(
        self,
        transcript
    ):

        logger.info("=" * 70)

        logger.info("Building Context...")

        logger.info("=" * 70)

        context = ""

        for chunk in transcript["chunks"]:

            context += chunk["text"] + "\n\n"

        logger.info(

            f"Context Length : {len(context)}"

        )

        return context

    # =====================================================
    # Split Context
    # =====================================================

    def split_context(

        self,

        context,

        max_chars=MAX_CONTEXT_CHARS

    ):

        logger.info("=" * 70)

        logger.info("Splitting Context...")

        logger.info("=" * 70)

        chunks = []

        current = ""

        paragraphs = context.split("\n\n")

        for paragraph in paragraphs:

            if len(current) + len(paragraph) < max_chars:

                current += paragraph + "\n\n"

            else:

                chunks.append(

                    current

                )

                current = paragraph + "\n\n"

        if current:

            chunks.append(

                current

            )

        logger.info(

            f"Total Parts : {len(chunks)}"

        )

        return chunks

    # =====================================================
    # Statistics
    # =====================================================

    def build_statistics(

        self,

        start_time,

        total_parts,

        cached=False

    ):

        return {

            "execution_time": round(

                time.time() - start_time,

                2

            ),

            "parts": total_parts,

            "cached": cached

        }

    # =====================================================
    # Update Feature
    # =====================================================

    def update_feature(

        self,

        lecture_id,

        feature_name,

        value=True

    ):

        metadata = self.load_metadata(

            lecture_id

        )

        metadata["features"][

            feature_name

        ] = value

        self.save_metadata(

            lecture_id,

            metadata

        )
        # =====================================================
    # Ensure Pipeline
    # =====================================================

    def ensure_pipeline(

        self,

        lecture_id

    ):

        logger.info("=" * 70)
        logger.info("Ensuring AI Pipeline...")
        logger.info("=" * 70)

        metadata = self.load_metadata(

            lecture_id

        )

        pipeline = metadata["pipeline"]

        # ----------------------------------------
        # Audio
        # ----------------------------------------

        if not pipeline["audio_extracted"]:

            logger.info(

                "Audio not found. Extracting..."

            )

            self.audio_service.process(

                lecture_id

            )

            metadata = self.load_metadata(

                lecture_id

            )

            pipeline = metadata["pipeline"]

        # ----------------------------------------
        # Transcript + Chunking
        # ----------------------------------------

        if not pipeline["transcription_completed"]:

            logger.info(

                "Transcript not found. Generating..."

            )

            self.transcription_service.process(

                lecture_id

            )

            metadata = self.load_metadata(

                lecture_id

            )

            pipeline = metadata["pipeline"]

        # ----------------------------------------
        # Embeddings
        # ----------------------------------------

        if not pipeline["embedding_completed"]:

            logger.info(

                "Embeddings not found. Generating..."

            )

            self.embedding_service.process(

                lecture_id

            )

            metadata = self.load_metadata(

                lecture_id

            )

            pipeline = metadata["pipeline"]

        logger.info(

            "Pipeline Ready."

        )
    # =====================================================
    # LLM Response
    # =====================================================

    def generate_llm_response(
        self,
        prompt
    ):

        logger.info("=" * 70)

        logger.info("Calling LLM...")

        logger.info("=" * 70)

        return self.llm.invoke(prompt)