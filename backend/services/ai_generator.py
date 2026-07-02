"""
=========================================================
AI Lecture Assistant
AI Generator Base Class
=========================================================
"""

import logging
from abc import ABC
from time import time

from backend.services.base_ai_service import BaseAIService


logger = logging.getLogger(__name__)


class AIGenerator(BaseAIService, ABC):

    """
    Generic AI Generator

    Summary
    Notes
    Quiz
    Flashcards
    Mindmap

    all inherit from this class.
    """

    def __init__(

        self,

        service_name,

        prompt_name,

        cache_prefix,

        supported_types

    ):

        super().__init__()

        self.service_name = service_name

        self.prompt_name = prompt_name

        self.cache_prefix = cache_prefix

        self.supported_types = supported_types

        logger.info("=" * 70)

        logger.info(f"{service_name} Initialized")

        logger.info("=" * 70)

    # =====================================================
    # Build Chunk Prompt
    # =====================================================

    def build_chunk_prompt(

        self,

        context,

        generation_type

    ):

        return self.prompt_manager.format_prompt(

            f"{self.prompt_name}_chunk",

            context=context,

            generation_type=generation_type

        )
    # =====================================================
    # Build Merge Prompt
    # =====================================================

    def build_merge_prompt(

        self,

        context,

        generation_type

    ):

        return self.prompt_manager.format_prompt(

            f"{self.prompt_name}_merge",

            context=context,

            generation_type=generation_type

        )
    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

            "service": self.service_name,

            "prompt": self.prompt_name,

            "cache_prefix": self.cache_prefix,

            "supported_types": self.supported_types,

            "llm": self.llm.health_check()

        }
    # =====================================================
    # Validate Generation Type
    # =====================================================

    def validate_type(

        self,

        generation_type

    ):

        generation_type = generation_type.lower().strip()

        if generation_type == "all":

            return "all"

        if generation_type not in self.supported_types:

            raise ValueError(

                f"""

    Invalid Type : {generation_type}

    Supported Types

    {self.supported_types}

    """

            )

        return generation_type
    
    # =====================================================
    # Cache File Name
    # =====================================================

    def get_cache_filename(

        self,

        generation_type

    ):

        extension = ".md"

        return (

            f"{self.cache_prefix}_"

            f"{generation_type}"

            f"{extension}"

        )
    # =====================================================
    # Generate Chunk
    # =====================================================

    def generate_chunk(

        self,

        context,

        generation_type

    ):

        logger.info(

            "Generating Chunk..."

        )

        prompt = self.build_chunk_prompt(

            context,

            generation_type

        )

        response = self.generate_llm_response(
                    prompt
            )
        return response
    # =====================================================
    # Merge Chunks
    # =====================================================

    def merge_chunks(

        self,

        partial_outputs,

        generation_type

    ):

        logger.info(

            "Merging Outputs..."

        )

        context = "\n\n".join(

            partial_outputs

        )

        prompt = self.build_merge_prompt(

            context,

            generation_type

        )

        response = self.generate_llm_response(
        prompt
        )

        return response
    
    # =====================================================
    # Save Output
    # =====================================================

    def save_output(

        self,

        lecture_id,

        generation_type,

        content

    ):

        filename = self.get_cache_filename(

            generation_type

        )

        path = self.cache.cache_path(

            lecture_id,

            filename

        )

        self.cache.save_cache(

            path,

            content

        )

        return path
    # =====================================================
    # Build Response
    # =====================================================

    def build_response(

        self,

        output,

        generation_type,

        cached,

        statistics

    ):

        return {

            "type": generation_type,

            "cached": cached,

            "output": output,

            "statistics": statistics

        }
    # =====================================================
    # Generate
    # =====================================================

    def generate(

        self,

        lecture_id,

        generation_type,

        use_cache=True

    ):

        start = time.time()

        generation_type = self.validate_type(

            generation_type

        )

        filename = self.get_cache_filename(

            generation_type

        )

        cache_path = self.cache.cache_path(

            lecture_id,

            filename

        )

        # ----------------------------------------
        # Cache
        # ----------------------------------------

        if use_cache and cache_path.exists():

            logger.info(

                "Loaded From Cache."

            )

            output = self.cache.load_cache(

                cache_path

            )

            return self.build_response(

                output,

                generation_type,

                True,

                self.build_statistics(

                    start,

                    0,

                    True

                )

            )

        # ----------------------------------------
        # Transcript
        # ----------------------------------------

        transcript = self.load_transcript(

            lecture_id

        )

        context = self.build_context(

            transcript

        )

        parts = self.split_context(

            context

        )

        outputs = []

        # ----------------------------------------
        # Generate
        # ----------------------------------------

        for part in parts:

            outputs.append(

                self.generate_chunk(

                    part,

                    generation_type

                )

            )

        # ----------------------------------------
        # Merge
        # ----------------------------------------

        final_output = self.merge_chunks(

            outputs,

            generation_type

        )

        # ----------------------------------------
        # Save
        # ----------------------------------------

        self.save_output(

            lecture_id,

            generation_type,

            final_output

        )

        # ----------------------------------------
        # Metadata
        # ----------------------------------------

        self.update_feature(

            lecture_id,

            f"{self.cache_prefix}_generated"

        )

        return self.build_response(

            final_output,

            generation_type,

            False,

            self.build_statistics(

                start,

                len(parts),

                False

            )

        )