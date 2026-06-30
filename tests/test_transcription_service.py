"""
=========================================================
AI Lecture Assistant
Test Transcription Service
=========================================================
"""

import time

from backend.services.transcription_service import TranscriptionService


def print_summary(metadata):

    print()

    print("=" * 70)

    print("TRANSCRIPTION SUMMARY")

    print("=" * 70)

    print()

    print(f"Lecture Name      : {metadata['lecture']['lecture_name']}")

    print(f"Lecture ID        : {metadata['lecture']['lecture_id']}")

    print()

    print(f"Current Stage     : {metadata['processing']['current_stage']}")

    print()

    print(f"Total Chunks      : {metadata['statistics']['total_chunks']}")

    print(f"Total Words       : {metadata['statistics']['total_words']}")

    print(f"Total Duration    : {metadata['statistics']['total_duration']} sec")

    print()

    print(f"Transcript File   : {metadata['files']['transcript_path']}")

    print()

    print("=" * 70)


def main():

    lecture_id = input(

        "Enter Lecture ID : "

    ).strip()

    service = TranscriptionService()

    start = time.time()

    metadata = service.process(

        lecture_id

    )

    end = time.time()

    print_summary(

        metadata

    )

    print()

    print(

        f"Execution Time : {round(end-start,2)} sec"

    )



if __name__ == "__main__":

    main()