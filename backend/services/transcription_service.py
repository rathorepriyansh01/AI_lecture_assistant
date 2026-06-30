"""
=========================================================
AI Lecture Assistant
Production Transcription Service
=========================================================

Responsibilities
----------------
1. Load metadata
2. Read audio.wav
3. Run Faster Whisper
4. Dynamic Chunking
5. Save transcript.json
6. Update Metadata
"""

import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path

import torch
from faster_whisper import WhisperModel

from config.settings import WHISPER_MODEL
from backend.utils.metadata_manager import MetadataManager

# ==========================================================
# CONFIGURATION
# ==========================================================

MAX_WORDS = 180

MAX_DURATION = 20

MIN_WORDS = 8

BEAM_SIZE = 3

SEGMENT_OVERLAP = 3

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)


class TranscriptionService:

    def __init__(self):

        self.manager = MetadataManager()

        self.device = self.detect_device()

        self.compute_type = (

            "float16"

            if self.device == "cuda"

            else "int8"

        )

        logger.info("=" * 70)

        logger.info("Loading Faster Whisper...")

        self.model = WhisperModel(

            WHISPER_MODEL,

            device=self.device,

            compute_type=self.compute_type

        )

        logger.info("Model Loaded Successfully.")

        logger.info(f"Device : {self.device}")

        logger.info(f"Model  : {WHISPER_MODEL}")

        logger.info("=" * 70)
    
        # =====================================================
    # Detect Device
    # =====================================================

    def detect_device(self):

        if torch.cuda.is_available():

            logger.info("CUDA Available")

            return "cuda"

        logger.info("CUDA Not Available")

        return "cpu"

    # =====================================================
    # Clean Text
    # =====================================================

    def clean_text(self, text: str):

        if text is None:

            return ""

        text = text.replace("\n", " ")

        text = text.replace("\t", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # =====================================================
    # Word Count
    # =====================================================

    def word_count(self, text):

        return len(text.split())

    # =====================================================
    # Format Timestamp
    # =====================================================

    def format_timestamp(self, seconds):

        seconds = int(seconds)

        hours = seconds // 3600

        minutes = (seconds % 3600) // 60

        seconds = seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # =====================================================
    # Validate Segment
    # =====================================================

    def is_valid_segment(self, text):

        text = self.clean_text(text)

        if self.word_count(text) < MIN_WORDS:

            return False

        return True

    # =====================================================
    # Create Chunk Metadata
    # =====================================================

    def create_metadata(

        self,

        lecture_name,

        chunk_id,

        start,

        end,

        text

    ):

        return {

            "lecture_name": lecture_name,

            "chunk_id": chunk_id,

            "start": round(start, 2),

            "end": round(end, 2),

            "duration": round(

                end - start,

                2

            ),

            "word_count": self.word_count(text),

            "char_count": len(text),

            "text": text

        }

    # =====================================================
    # Load Lecture Metadata
    # =====================================================

    def load_lecture(self, lecture_id):

        metadata = self.manager.load(

            lecture_id

        )

        audio_path = Path(

            metadata["files"]["audio_path"]

        )

        if not audio_path.exists():

            raise FileNotFoundError(

                f"Audio file not found : {audio_path}"

            )

        lecture_name = metadata["lecture"][

            "lecture_name"

        ]

        lecture_folder = audio_path.parent

        return (

            metadata,

            lecture_name,

            lecture_folder,

            audio_path

        )
        # =====================================================
    # Dynamic Chunking with Segment Overlap
    # =====================================================

    def create_dynamic_chunks(

        self,

        segments,

        lecture_name

    ):

        logger.info("=" * 70)

        logger.info("Building Dynamic Chunks...")

        logger.info("=" * 70)

        chunks = []

        current_segments = []

        chunk_id = 1

        for segment in segments:

            text = self.clean_text(

                segment.text

            )

            if not text:

                continue

            if self.word_count(text) < 2:

                continue

            current_segments.append(

                {

                    "start": segment.start,

                    "end": segment.end,

                    "text": text

                }

            )

            # ------------------------------------------
            # Current Chunk Statistics
            # ------------------------------------------

            chunk_text = " ".join(

                seg["text"]

                for seg in current_segments

            )

            total_words = self.word_count(

                chunk_text

            )

            duration = (

                current_segments[-1]["end"]

                -

                current_segments[0]["start"]

            )

            # ------------------------------------------
            # Save Chunk
            # ------------------------------------------

            if (

                total_words >= MAX_WORDS

                or

                duration >= MAX_DURATION

            ):

                chunks.append(

                    self.create_metadata(

                        lecture_name=lecture_name,

                        chunk_id=chunk_id,

                        start=current_segments[0]["start"],

                        end=current_segments[-1]["end"],

                        text=chunk_text

                    )

                )

                logger.info(

                    f"Chunk {chunk_id} Created "

                    f"| Words : {total_words} "

                    f"| Duration : {round(duration,2)} sec"

                )

                chunk_id += 1

                # ======================================
                # Segment Overlap
                # ======================================

                overlap = current_segments[

                    -SEGMENT_OVERLAP:

                ]

                current_segments = overlap.copy()

        # ------------------------------------------
        # Save Remaining Chunk
        # ------------------------------------------

        if len(current_segments) > 0:

            chunk_text = " ".join(

                seg["text"]

                for seg in current_segments

            )

            if self.is_valid_segment(

                chunk_text

            ):

                chunks.append(

                    self.create_metadata(

                        lecture_name=lecture_name,

                        chunk_id=chunk_id,

                        start=current_segments[0]["start"],

                        end=current_segments[-1]["end"],

                        text=chunk_text

                    )

                )

                logger.info(

                    f"Final Chunk {chunk_id} Saved."

                )

        logger.info("=" * 70)

        logger.info(

            f"Total Chunks Created : {len(chunks)}"

        )

        logger.info("=" * 70)

        return chunks
        # =====================================================
    # Transcribe Audio
    # =====================================================

    def transcribe_audio(

        self,

        audio_path,

        lecture_name

    ):

        logger.info("=" * 70)

        logger.info(

            f"Processing Lecture : {lecture_name}"

        )

        logger.info("=" * 70)

        start_time = time.time()

        # ---------------------------------------------
        # Whisper Inference
        # ---------------------------------------------

        segments, info = self.model.transcribe(

            str(audio_path),

            beam_size=BEAM_SIZE,

            vad_filter=True,

            condition_on_previous_text=False,

            language="en"

        )

        # ---------------------------------------------
        # Dynamic Chunking
        # ---------------------------------------------

        chunks = self.create_dynamic_chunks(

            segments,

            lecture_name

        )

        processing_time = round(

            time.time() - start_time,

            2

        )

        logger.info(

            f"Language : {info.language}"

        )

        logger.info(

            f"Duration : {round(info.duration,2)} sec"

        )

        logger.info(

            f"Processing Time : {processing_time} sec"

        )

        logger.info(

            f"Chunks Generated : {len(chunks)}"

        )

        return {

            "chunks": chunks,

            "language": info.language,

            "duration": round(

                info.duration,

                2

            ),

            "processing_time": processing_time

        }

    # =====================================================
    # Build Transcript Dictionary
    # =====================================================

    def build_transcript(

        self,

        lecture_name,

        result

    ):

        chunks = result["chunks"]

        total_words = sum(

            chunk["word_count"]

            for chunk in chunks

        )

        total_duration = round(

            sum(

                chunk["duration"]

                for chunk in chunks

            ),

            2

        )

        transcript = {

            "lecture_name": lecture_name,

            "created_at": datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            ),

            "total_chunks": len(chunks),

            "total_words": total_words,

            "total_duration": total_duration,

            "model": WHISPER_MODEL,

            "device": self.device,

            "chunks": chunks

        }

        return transcript
    
        # =====================================================
    # Save Transcript JSON
    # =====================================================

    def save_transcript(

        self,

        lecture_folder,

        transcript

    ):

        transcript_path = (

            lecture_folder /

            "transcript.json"

        )

        logger.info("=" * 70)

        logger.info(

            "Saving transcript.json..."

        )

        with open(

            transcript_path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                transcript,

                f,

                indent=4,

                ensure_ascii=False

            )

        logger.info(

            "transcript.json Saved Successfully."

        )

        logger.info(

            f"Location : {transcript_path}"

        )

        logger.info("=" * 70)

        return transcript_path

    # =====================================================
    # Verify Transcript
    # =====================================================

    def verify_transcript(

        self,

        transcript_path

    ):

        if not transcript_path.exists():

            raise FileNotFoundError(

                "transcript.json not found."

            )

        with open(

            transcript_path,

            "r",

            encoding="utf-8"

        ) as f:

            data = json.load(f)

        logger.info("=" * 70)

        logger.info("Transcript Verification")

        logger.info("=" * 70)

        logger.info(

            f"Lecture : {data['lecture_name']}"

        )

        logger.info(

            f"Chunks : {data['total_chunks']}"

        )

        logger.info(

            f"Words : {data['total_words']}"

        )

        logger.info(

            f"Duration : {data['total_duration']} sec"

        )

        logger.info("=" * 70)

        return True
    
        # =====================================================
    # Update Metadata
    # =====================================================

    def update_metadata(

        self,

        lecture_id,

        transcript_path,

        transcript,

        processing_time

    ):

        logger.info("=" * 70)

        logger.info("Updating Metadata...")

        logger.info("=" * 70)

        # ---------------------------------------------
        # Files
        # ---------------------------------------------

        self.manager.update_files(

            lecture_id,

            transcript_path=str(

                transcript_path

            )

        )

        # ---------------------------------------------
        # Statistics
        # ---------------------------------------------

        self.manager.update_statistics(

            lecture_id,

            total_chunks=transcript["total_chunks"],

            total_words=transcript["total_words"],

            total_duration=transcript["total_duration"]

        )

        # ---------------------------------------------
        # Models
        # ---------------------------------------------

        self.manager.update_models(

            lecture_id,

            whisper_model=WHISPER_MODEL

        )

        # ---------------------------------------------
        # Pipeline
        # ---------------------------------------------

        self.manager.update_pipeline(

            lecture_id,

            transcription_completed=True

        )

        # ---------------------------------------------
        # Processing
        # ---------------------------------------------

        self.manager.update_processing(

            lecture_id,

            current_stage="Transcription Completed",

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
    # Process Lecture
    # =====================================================

    def process(

        self,

        lecture_id

    ):

        logger.info("=" * 70)

        logger.info(

            "Starting Transcription Pipeline..."

        )

        logger.info("=" * 70)

        overall_start = time.time()

        try:

            # -----------------------------------------
            # Load Lecture
            # -----------------------------------------

            metadata, lecture_name, lecture_folder, audio_path = (

                self.load_lecture(

                    lecture_id

                )

            )

            logger.info(

                f"Lecture : {lecture_name}"

            )

            logger.info(

                f"Audio   : {audio_path.name}"

            )

            # -----------------------------------------
            # Whisper Transcription
            # -----------------------------------------

            result = self.transcribe_audio(

                audio_path,

                lecture_name

            )

            # -----------------------------------------
            # Build Transcript
            # -----------------------------------------

            transcript = self.build_transcript(

                lecture_name,

                result

            )

            # -----------------------------------------
            # Save Transcript
            # -----------------------------------------

            transcript_path = self.save_transcript(

                lecture_folder,

                transcript

            )

            # -----------------------------------------
            # Verify JSON
            # -----------------------------------------

            self.verify_transcript(

                transcript_path

            )

            # -----------------------------------------
            # Metadata Update
            # -----------------------------------------

            self.update_metadata(

                lecture_id=lecture_id,

                transcript_path=transcript_path,

                transcript=transcript,

                processing_time=result["processing_time"]

            )

            total_time = round(

                time.time() - overall_start,

                2

            )

            logger.info("=" * 70)

            logger.info(

                "TRANSCRIPTION COMPLETED"

            )

            logger.info("=" * 70)

            logger.info(

                f"Lecture        : {lecture_name}"

            )

            logger.info(

                f"Chunks         : {transcript['total_chunks']}"

            )

            logger.info(

                f"Words          : {transcript['total_words']}"

            )

            logger.info(

                f"Duration       : {transcript['total_duration']} sec"

            )

            logger.info(

                f"Total Time     : {total_time} sec"

            )

            logger.info("=" * 70)

            return self.manager.load(

                lecture_id

            )

        except Exception as e:

            logger.exception(

                "Transcription Failed."

            )

            self.manager.update_processing(

                lecture_id,

                current_stage="Failed",

                last_error=str(e)

            )

            raise