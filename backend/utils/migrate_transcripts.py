"""
=========================================================
AI Lecture Assistant

Transcript Migration Utility

Version : 1.0
=========================================================

Purpose

Old Transcript
        ↓
New Transcript Schema

Automatically adds

✓ version
✓ lecture_id
✓ lecture_name
✓ created_at
✓ duration
✓ char_count
"""

import json
import logging
from pathlib import Path

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)


ROOT = Path(__file__).resolve().parents[2]

LECTURES_DIR = ROOT / "data" / "lectures"


def migrate_lecture(

    lecture_folder: Path

):

    metadata_file = lecture_folder / "metadata.json"

    transcript_file = lecture_folder / "transcript.json"

    if not metadata_file.exists():

        logger.warning(

            f"Metadata Missing : {lecture_folder.name}"

        )

        return

    if not transcript_file.exists():

        logger.warning(

            f"Transcript Missing : {lecture_folder.name}"

        )

        return

    with open(

        metadata_file,

        "r",

        encoding="utf-8"

    ) as f:

        metadata = json.load(f)

    with open(

        transcript_file,

        "r",

        encoding="utf-8"

    ) as f:

        transcript = json.load(f)

    # -------------------------------------------------

    lecture = metadata.get("lecture", {})

    statistics = metadata.get("statistics", {})

    models = metadata.get("models", {})

    lecture_id = lecture.get(

        "lecture_id",

        lecture_folder.name

    )

    lecture_name = lecture.get(

        "lecture_name",

        transcript.get(

            "lecture_name",

            lecture_folder.name

        )

    )

    created_at = lecture.get(

        "created_at",

        transcript.get(

            "created_at",

            ""

        )

    )

    # -------------------------------------------------

    transcript["version"] = "1.0"

    transcript["lecture_id"] = lecture_id

    transcript["lecture_name"] = lecture_name

    transcript["created_at"] = created_at

    transcript["model"] = transcript.get(

        "model",

        models.get(

            "whisper",

            ""

        )

    )

    transcript["device"] = transcript.get(

        "device",

        "cuda"

    )

    transcript["total_chunks"] = len(

        transcript["chunks"]

    )

    transcript["total_duration"] = transcript.get(

        "total_duration",

        statistics.get(

            "duration",

            0

        )

    )

    # -------------------------------------------------

    total_words = 0

    for i, chunk in enumerate(

        transcript["chunks"],

        start=1

    ):

        chunk["lecture_id"] = lecture_id

        chunk["lecture_name"] = lecture_name

        chunk["chunk_id"] = chunk.get(

            "chunk_id",

            i

        )

        chunk["duration"] = round(

            chunk["end"] - chunk["start"],

            2

        )

        chunk["word_count"] = len(

            chunk["text"].split()

        )

        chunk["char_count"] = len(

            chunk["text"]

        )

        total_words += chunk["word_count"]

    transcript["total_words"] = total_words

    # -------------------------------------------------

    with open(

        transcript_file,

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

        f"Migrated : {lecture_name}"

    )


def main():

    logger.info("=" * 70)

    logger.info(

        "Transcript Migration Started"

    )

    logger.info("=" * 70)

    count = 0

    for lecture in LECTURES_DIR.iterdir():

        if lecture.is_dir():

            migrate_lecture(

                lecture

            )

            count += 1

    logger.info("=" * 70)

    logger.info(

        f"Migration Completed : {count} lectures"

    )

    logger.info("=" * 70)


if __name__ == "__main__":

    main()