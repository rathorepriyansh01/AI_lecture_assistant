"""
=========================================================
AI Lecture Assistant
Notes Service
=========================================================
"""

import json
import time
import logging
from pathlib import Path
from pathlib import Path
from datetime import datetime
import time

from backend.core.llm import LLMManager
from backend.core.prompt_manager import PromptManager
from backend.services.base_ai_service import BaseAIService
from backend.utils.cache_manager import CacheManager
from backend.utils.metadata_manager import MetadataManager

logger = logging.getLogger(__name__)


class NotesService:

    def __init__(self):

        logger.info("=" * 70)
        logger.info("Initializing Notes Service...")
        logger.info("=" * 70)

        self.llm = LLMManager()

        self.prompt_manager = PromptManager()

        self.cache = CacheManager()

        self.manager = MetadataManager()

        logger.info("Notes Service Ready.")

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

            "status": "healthy",

            "service": "Notes Service",

            "llm": self.llm.health_check()

        }
    # =====================================================
    # Load Transcript
    # =====================================================

    def load_transcript(
        self,
        lecture_id
    ):

        lecture_dir = (

            Path(__file__).resolve().parents[2]

            / "data"

            / "lectures"

            / lecture_id

        )

        transcript_path = lecture_dir / "transcript.json"

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
    # Generate Chunk Notes
    # =====================================================

    def generate_chunk_notes(
        self,
        context,
        notes_type
    ):

        logger.info("=" * 70)
        logger.info("Generating Chunk Notes...")
        logger.info("=" * 70)

        prompt = self.prompt_manager.format_prompt(

            "notes_chunk_prompt",

            context=context,

            notes_type=notes_type

        )

        return self.llm.invoke(prompt)
    # =====================================================
    # Merge Notes
    # =====================================================

    def merge_notes(
        self,
        partial_notes,
        notes_type
    ):

        logger.info("=" * 70)
        logger.info("Merging Notes...")
        logger.info("=" * 70)

        context = "\n\n".join(partial_notes)

        prompt = self.prompt_manager.format_prompt(

            "notes_merge_prompt",

            context=context,

            notes_type=notes_type

        )
        

        return self.llm.invoke(prompt)
    # =====================================================
    # Generate Notes
    # =====================================================

    def generate(
        self,
        lecture_id,
        notes_type,
        use_cache=True
    ):
        start = time.time()
        logger.info("=" * 70)
        logger.info("Generating Notes...")
        logger.info("=" * 70)

        lecture_dir = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "lectures"
            / lecture_id
)

        notes_file = lecture_dir / f"notes_{notes_type}.md"

        if use_cache and notes_file.exists():

            logger.info("=" * 70)
            logger.info("Notes Loaded From Cache")
            logger.info("=" * 70)

            with open(
            notes_file,
            "r",
            encoding="utf-8"
                ) as f:

                notes = f.read()

            return {

            "notes": notes,

            "cached": True,

            "statistics": {

                "execution_time": 0,

                "parts": 0

            }

        }

        transcript = self.load_transcript(
            lecture_id
        )

        context = self.build_context(
            transcript
        )

        parts = self.split_context(
            context
        )

        partial_notes = []

        total = len(parts)

        for i, part in enumerate(parts, start=1):

            logger.info(

                f"Processing Part {i}/{total}"

            )

            notes = self.generate_chunk_notes(

                part,

                notes_type

            )

            partial_notes.append(notes)

        logger.info("=" * 70)
        logger.info("Merging Final Notes...")
        logger.info("=" * 70)

        final_notes = self.merge_notes(
        partial_notes,
        notes_type
        )

        # ==========================
        # Save Notes
        # ==========================

        with open(
            notes_file,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(
                final_notes
            )
        # =====================================
        # Update Metadata
        # =====================================

        metadata = self.manager.load(
            lecture_id
        )

        metadata["features"]["notes_generated"] = True

        metadata["exports"][
            f"notes_{notes_type}_path"
        ] = str(notes_file)

        metadata["lecture"]["last_updated"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.manager.save(
            lecture_id,
            metadata
        )
        execution_time = round(

        time.time() - start,2)

        return {

    "notes": final_notes,

    "cached": False,

    "notes_type": notes_type,

    "statistics": {

        "execution_time": execution_time,

        "parts": len(parts)

    }

}
        
    def split_context(

        self,

        context,

        max_chars=12000

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