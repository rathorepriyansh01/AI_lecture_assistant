"""
=========================================================
AI Lecture Assistant
Audio Service
Production Version
=========================================================
"""

import time
from pathlib import Path

import ffmpeg

from backend.utils.metadata_manager import MetadataManager


class AudioService:

    def __init__(self):

        self.manager = MetadataManager()

    # =====================================================
    # Extract Audio
    # =====================================================

    def extract_audio(
        self,
        video_path: Path,
        audio_path: Path
    ):

        (
            ffmpeg
            .input(str(video_path))
            .output(
                str(audio_path),

                ac=1,             # Mono

                ar=16000,         # 16 KHz

                format="wav"
            )
            .overwrite_output()
            .run(
                quiet=True
            )
        )

    # =====================================================
    # Audio Duration
    # =====================================================

    def get_audio_duration(
        self,
        audio_path: Path
    ):

        probe = ffmpeg.probe(
            str(audio_path)
        )

        duration = float(

            probe["format"]["duration"]

        )

        return round(duration, 2)

    # =====================================================
    # Process
    # =====================================================

    def process(
        self,
        lecture_id: str
    ):

        start_time = time.time()

        metadata = self.manager.load(
            lecture_id
        )

        video_path = Path(

            metadata["files"]["video_path"]

        )

        lecture_folder = video_path.parent

        audio_path = lecture_folder / "audio.wav"

        # --------------------------------------------
        # Extract Audio
        # --------------------------------------------

        self.extract_audio(

            video_path,

            audio_path

        )

        duration = self.get_audio_duration(

            audio_path

        )

        processing_time = round(

            time.time() - start_time,

            2

        )

        # --------------------------------------------
        # Update Files
        # --------------------------------------------

        self.manager.update_files(

            lecture_id,

            audio_path=str(audio_path)

        )

        # --------------------------------------------
        # Update Statistics
        # --------------------------------------------

        self.manager.update_statistics(

            lecture_id,

            audio_duration=duration

        )

        # --------------------------------------------
        # Update Pipeline
        # --------------------------------------------

        self.manager.update_pipeline(

            lecture_id,

            audio_extracted=True

        )

        # --------------------------------------------
        # Update Processing
        # --------------------------------------------

        self.manager.update_processing(

            lecture_id,

            current_stage="Audio Ready",

            processing_time=processing_time,

            last_error=""

        )

        return self.manager.load(

            lecture_id

        )