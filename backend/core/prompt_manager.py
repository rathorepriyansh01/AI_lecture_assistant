"""
=========================================================
AI Lecture Assistant
Prompt Manager
Production Version
=========================================================

Responsibilities
----------------
1. Load prompts
2. Cache prompts
3. Format prompts
"""

from pathlib import Path
import logging

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class PromptManager:

    _cache = {}

    def __init__(self):

        self.prompt_dir = (

            Path(__file__).parent.parent /

            "prompts"

        )

    # =====================================================
    # Load Prompt
    # =====================================================

    def get_prompt(

        self,

        prompt_name

    ):

        filename = f"{prompt_name}.txt"

        if filename in self._cache:

            return self._cache[filename]

        file_path = self.prompt_dir / filename

        if not file_path.exists():

            raise FileNotFoundError(

                f"Prompt not found : {filename}"

            )

        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as f:

            prompt = f.read()

        self._cache[filename] = prompt

        logger.info(

            f"Prompt Loaded : {filename}"

        )

        return prompt

    # =====================================================
    # Format Prompt
    # =====================================================

    def format_prompt(

        self,

        prompt_name,

        **kwargs

    ):

        prompt = self.get_prompt(

            prompt_name

        )

        return prompt.format(

            **kwargs

        )

    # =====================================================
    # Clear Cache
    # =====================================================

    def clear_cache(self):

        self._cache.clear()

        logger.info(

            "Prompt Cache Cleared."

        )

    # =====================================================
    # Available Prompts
    # =====================================================

    def available_prompts(self):

        return [

            file.stem

            for file in self.prompt_dir.glob("*.txt")

        ]