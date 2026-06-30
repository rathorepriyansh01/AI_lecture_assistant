"""
=========================================================
AI Lecture Assistant
Video Service
Production Version
=========================================================

Responsibilities
----------------
1. Validate uploaded video
2. Generate unique Lecture ID
3. Create lecture folder
4. Save uploaded video
5. Create production metadata
"""

import json
import shutil
import uuid
from pathlib import Path
from datetime import datetime

from config.settings import LECTURES_DIR
from config.constants import VIDEO_EXTENSIONS


class VideoService:

    def __init__(self):

        self.lectures_dir = Path(LECTURES_DIR)

    # =====================================================
    # Validate Video
    # =====================================================

    def validate_video(self, video_path: str):

        video = Path(video_path)

        if not video.exists():

            raise FileNotFoundError(
                f"Video not found : {video}"
            )

        if video.suffix.lower() not in VIDEO_EXTENSIONS:

            raise ValueError(
                f"Unsupported video format : {video.suffix}"
            )

        return video

    # =====================================================
    # Create Default Metadata
    # =====================================================

    def create_metadata(

        self,

        lecture_id,

        video_file,

        saved_video_path

    ):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        metadata = {

            "version": {

                "project_version": "1.0.0",

                "metadata_version": "1.0",

                "created_by": "AI Lecture Assistant"

            },

            "lecture": {

                "lecture_id": lecture_id,

                "lecture_name": video_file.stem,

                "original_filename": video_file.name,

                "course_name": "",

                "uploaded_at": now,

                "last_updated": now

            },

            "pipeline": {

                "upload_completed": True,

                "audio_extracted": False,

                "transcription_completed": False,

                "chunking_completed": False,

                "embedding_completed": False,

                "vector_db_completed": False,

                "ready_for_chat": False

            },

            "files": {

                "video_path": str(saved_video_path),

                "audio_path": "",

                "transcript_path": "",

                "chunk_path": "",

                "thumbnail_path": ""

            },

            "statistics": {

                "video_duration": 0,

                "audio_duration": 0,

                "total_chunks": 0,

                "total_words": 0,

                "total_characters": 0,

                "language": ""

            },

            "models": {

                "whisper_model": "",

                "embedding_model": "",

                "llm_model": ""

            },

            "processing": {

                "current_stage": "Uploaded",

                "processing_time": 0,

                "last_error": ""

            },

            "features": {

                "summary_generated": False,

                "notes_generated": False,

                "quiz_generated": False,

                "flashcards_generated": False,

                "mindmap_generated": False

            },

            "exports": {

                "summary_path": "",

                "notes_path": "",

                "quiz_path": "",

                "flashcards_path": "",

                "mindmap_path": ""

            }

        }

        return metadata

    # =====================================================
    # Create Lecture
    # =====================================================

    def create_lecture(

        self,

        video_path: str

    ):

        video = self.validate_video(
            video_path
        )

        lecture_id = str(uuid.uuid4())

        lecture_folder = (

            self.lectures_dir /

            lecture_id

        )

        lecture_folder.mkdir(

            parents=True,

            exist_ok=True

        )

        destination = (

            lecture_folder /

            "video.mp4"

        )

        shutil.copy2(

            video,

            destination

        )

        metadata = self.create_metadata(

            lecture_id,

            video,

            destination

        )

        metadata_path = (

            lecture_folder /

            "metadata.json"

        )

        with open(

            metadata_path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                metadata,

                f,

                indent=4,

                ensure_ascii=False

            )

        return metadata

    # =====================================================
    # Read Metadata
    # =====================================================

    def load_metadata(

        self,

        lecture_id

    ):

        metadata_path = (

            self.lectures_dir /

            lecture_id /

            "metadata.json"

        )

        if not metadata_path.exists():

            raise FileNotFoundError(

                "Metadata not found."

            )

        with open(

            metadata_path,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    # =====================================================
    # Update Metadata
    # =====================================================

    def save_metadata(

        self,

        lecture_id,

        metadata

    ):

        metadata["lecture"]["last_updated"] = (

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

        metadata_path = (

            self.lectures_dir /

            lecture_id /

            "metadata.json"

        )

        with open(

            metadata_path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                metadata,

                f,

                indent=4,

                ensure_ascii=False

            )