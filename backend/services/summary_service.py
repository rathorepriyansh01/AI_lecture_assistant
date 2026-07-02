import json
import logging
import time
from pathlib import Path
from datetime import datetime

from backend.core.llm import LLMManager
from backend.core.prompt_manager import PromptManager
from backend.utils.metadata_manager import MetadataManager

logger = logging.getLogger(__name__)


class SummaryService:

    def __init__(self):
        from backend.utils.cache_manager import CacheManager
        self.cache = CacheManager()

        logger.info("=" * 70)
        logger.info("Initializing Summary Service...")
        logger.info("=" * 70)

        self.llm = LLMManager()

        self.prompt_manager = PromptManager()

        self.manager = MetadataManager()

        logger.info("Summary Service Ready.")

    def health_check(self):

        return {

            "status": "healthy",

            "llm": self.llm.health_check(),

            "prompts": self.prompt_manager.available_prompts()

        }
    def load_transcript(
    self,
    lecture_id
):

        project_root = Path(__file__).resolve().parents[2]

        transcript_path = (
            project_root
            / "data"
            / "lectures"
            / lecture_id
            / "transcript.json"
        )

        logger.info(f"Transcript Path : {transcript_path}")

        if not transcript_path.exists():

            raise FileNotFoundError(
                f"Transcript not found:\n{transcript_path}"
            )

        with open(
            transcript_path,
            "r",
            encoding="utf-8"
        ) as f:

            transcript = json.load(f)

        return transcript
    
    def build_context(

    self,

    transcript

):

        logger.info("Building Full Lecture Context...")

        context = ""

        for chunk in transcript["chunks"]:

            context += chunk["text"] + "\n\n"

        logger.info(

            f"Context Length : {len(context)}"

        )

        return context
    # ==========================================================
    # Split Context
    # ==========================================================

    def split_context(
        self,
        context: str,
        max_chars: int = 12000
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

                chunks.append(current)

                current = paragraph + "\n\n"

        if current:

            chunks.append(current)

        logger.info(f"Total Context Parts : {len(chunks)}")

        return chunks
    # ==========================================================
    # Build Summary Prompt
    # ==========================================================

    def build_summary_prompt(
        self,
        context: str,
        summary_type
    ):

        return self.prompt_manager.format_prompt(

            "summary",

            context=context,

            summary_type=summary_type

        )
    # ==========================================================
    # Generate Chunk Summary
    # ==========================================================

    def summary_chunk_prompt(
        self,
        context,
        summary_type="detailed"
    ):

        prompt = self.build_summary_prompt(

            context,

            summary_type

        )

        return self.llm.invoke(prompt)
    # =====================================================
    # Merge Partial Summaries
    # =====================================================

    def summary_merge_prompt(

        self,

        summaries,

        summary_type

    ):

        logger.info("=" * 70)
        logger.info("Merging Partial Summaries...")
        logger.info("=" * 70)

        merged = "\n\n".join(summaries)

        prompt = self.build_summary_prompt(

            merged,

            summary_type

        )

        final_summary = self.llm.invoke(

            prompt

        )

        return final_summary
    
    # =====================================================
    # Generate Summary
    # =====================================================

    def generate(

        self,

        lecture_id,

        summary_type="detailed",

        force=False,

        use_cache=True

    ):
        start = time.time()
        logger.info("=" * 70)
        logger.info("Generating Summary...")
        logger.info("=" * 70)

        summary_file = self.cache.get_summary_file(

            lecture_id,

            summary_type

        )
        if use_cache and summary_file.exists():

            logger.info("Summary Loaded From Cache.")

            return {

                "summary": self.cache.load_cache(summary_file),

                "cached": True,

                "summary_type": summary_type,

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
        partial_summaries = []

        for i, part in enumerate(parts):

            logger.info(

                f"Summarizing Part {i+1}/{len(parts)}"

            )

            summary = self.summary_chunk_prompt(

                part,

                summary_type

            )

            partial_summaries.append(

                summary

            )
        final_summary = self.summary_merge_prompt(

        partial_summaries,

        summary_type

        )
        self.cache.save_cache(

        summary_file,

        final_summary

        )
        metadata = self.manager.load(
            lecture_id
        )

        metadata["features"]["summary_generated"] = True

        metadata["lecture"]["last_updated"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.manager.save(
            lecture_id,
            metadata
)
        execution_time = round(

        time.time() - start,

        2

        )
        return {

            "summary": final_summary,

            "cached": False,

            "summary_type": summary_type,

            "statistics": {

                "execution_time": execution_time,

                "parts": len(parts)

            }

        }
    # =====================================================
    # Generate Summary By Type
    # =====================================================

    def generate_by_type(
        self,
        lecture_id: str,
        summary_type: str = "short",
        use_cache: bool = True
    ):

        summary_type = summary_type.lower().strip()

        available_types = [

            "short",

            "detailed",

            "bullet",

            "keypoints",

            "chapter",

            "all"

        ]

        if summary_type not in available_types:

            raise ValueError(

                f"""
    Invalid Summary Type : {summary_type}

    Available Types

    - short
    - detailed
    - bullet
    - keypoints
    - chapter
    - all
    """

            )

        logger.info("=" * 70)

        logger.info(f"Summary Type : {summary_type}")

        logger.info("=" * 70)

        # ============================================
        # Generate All Summary Types
        # ============================================

        if summary_type == "all":

            logger.info("Generating All Summary Types...")

            results = {}

            for summary in [

                "short",

                "detailed",

                "bullet",

                "keypoints",

                "chapter"

            ]:

                logger.info(f"Generating : {summary}")

                results[summary] = self.generate(

                    lecture_id=lecture_id,

                    summary_type=summary,

                    use_cache=use_cache

                )

            logger.info("=" * 70)

            logger.info("All Summaries Generated Successfully.")

            logger.info("=" * 70)

            return results

        # ============================================
        # Generate Single Summary
        # ============================================

        return self.generate(

            lecture_id=lecture_id,

            summary_type=summary_type,

            use_cache=use_cache

        )