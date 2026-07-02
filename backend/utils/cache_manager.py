"""
=========================================================
AI Lecture Assistant
Cache Manager
=========================================================
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CacheManager:
    # =====================================================
    # File Name Templates
    # =====================================================

    SUMMARY_TYPES = {

        "short": "summary_short.md",

        "detailed": "summary_detailed.md",

        "bullet": "summary_bullet.md",

        "keypoints": "summary_keypoints.md",

        "chapter": "summary_chapter.md"

    }


    NOTES_TYPES = {

        "short": "notes_short.md",

        "exam": "notes_exam.md",

        "detailed": "notes_detailed.md"

    }


    QUIZ_TYPES = {

        "easy": "quiz_easy.json",

        "medium": "quiz_medium.json",

        "hard": "quiz_hard.json"

    }


    FLASHCARD_FILE = "flashcards.json"

    MINDMAP_FILE = "mindmap.json"
    

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.lecture_root = self.project_root / "data" / "lectures"
        
    # =====================================================
    # Lecture Directory
    # =====================================================

    def lecture_directory(
        self,
        lecture_id: str
    ) -> Path:

        path = self.lecture_root / lecture_id

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    # =====================================================
    # Cache File Path
    # =====================================================

    def cache_path(
        self,
        lecture_id: str,
        filename: str
    ) -> Path:

        return self.lecture_directory(
            lecture_id
        ) / filename

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        lecture_id: str,
        filename: str
    ) -> bool:

        return self.cache_path(
            lecture_id,
            filename
        ).exists()

    # =====================================================
    # Save Text
    # =====================================================

    def save_text(
        self,
        lecture_id: str,
        filename: str,
        text: str
    ):

        path = self.cache_path(
            lecture_id,
            filename
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

        logger.info(f"Saved Cache : {path}")

    # =====================================================
    # Load Text
    # =====================================================

    def load_text(
        self,
        lecture_id: str,
        filename: str
    ) -> str:

        path = self.cache_path(
            lecture_id,
            filename
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    # =====================================================
    # Save JSON
    # =====================================================

    def save_json(
        self,
        lecture_id: str,
        filename: str,
        data: dict
    ):

        path = self.cache_path(
            lecture_id,
            filename
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        logger.info(f"Saved Cache : {path}")

    # =====================================================
    # Load JSON
    # =====================================================

    def load_json(
        self,
        lecture_id: str,
        filename: str
    ):

        path = self.cache_path(
            lecture_id,
            filename
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        lecture_id: str,
        filename: str
    ):

        path = self.cache_path(
            lecture_id,
            filename
        )

        if path.exists():

            path.unlink()

            logger.info(f"Deleted Cache : {path}")

    # =====================================================
    # Clear Lecture Cache
    # =====================================================

    def clear(
        self,
        lecture_id: str
    ):

        lecture_dir = self.lecture_directory(
            lecture_id
        )

        for file in lecture_dir.iterdir():

            if file.suffix in [
                ".md",
                ".json",
                ".txt"
            ]:

                if file.name not in [
                    "metadata.json",
                    "transcript.json"
                ]:

                    file.unlink()

        logger.info(
            f"Cache Cleared : {lecture_id}"
        )

    
    # =====================================================
    # Summary File
    # =====================================================

    def get_summary_file(
        self,
        lecture_id,
        summary_type="detailed"
    ):

        if summary_type not in self.SUMMARY_TYPES:

            raise ValueError(
                f"Unknown summary type : {summary_type}"
            )

        return self.cache_path(

            lecture_id,

            self.SUMMARY_TYPES[summary_type]

        )
    # =====================================================
    # Notes File
    # =====================================================

    def get_notes_file(
        self,
        lecture_id,
        notes_type="exam"
    ):

        if notes_type not in self.NOTES_TYPES:

            raise ValueError(
                f"Unknown notes type : {notes_type}"
            )

        return self.cache_path(

            lecture_id,

            self.NOTES_TYPES[notes_type]

        )
    # =====================================================
    # Quiz File
    # =====================================================

    def get_quiz_file(
        self,
        lecture_id,
        difficulty="medium"
    ):

        if difficulty not in self.QUIZ_TYPES:

            raise ValueError(
                f"Unknown difficulty : {difficulty}"
            )

        return self.cache_path(

            lecture_id,

            self.QUIZ_TYPES[difficulty]

        )
    # =====================================================
    # Flashcards
    # =====================================================

    def get_flashcards_file(
        self,
        lecture_id
    ):

        return self.cache_path(

            lecture_id,

            self.FLASHCARD_FILE

        )
    # =====================================================
    # Mindmap
    # =====================================================

    def get_mindmap_file(
        self,
        lecture_id
    ):

        return self.cache_path(

            lecture_id,

            self.MINDMAP_FILE

        )
    # =====================================================
    # Save Cache
    # =====================================================

    def save_cache(
        self,
        path,
        content
    ):

        path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:

            f.write(content)

        logger.info(

            f"Cache Saved : {path.name}"

        )

        
    # =====================================================
    # Load Cache
    # =====================================================

    def load_cache(
        self,
        path
    ):

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            return f.read()