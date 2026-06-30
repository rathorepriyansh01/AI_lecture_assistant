"""
=========================================================
AI Lecture Assistant
Metadata Manager
Production Version
=========================================================
"""

import json
from pathlib import Path
from datetime import datetime

from config.settings import LECTURES_DIR


class MetadataManager:

    def __init__(self):

        self.lectures_dir = Path(LECTURES_DIR)

    # =====================================================
    # Metadata Path
    # =====================================================

    def metadata_path(self, lecture_id):

        return (

            self.lectures_dir

            / lecture_id

            / "metadata.json"

        )

    # =====================================================
    # Load Metadata
    # =====================================================

    def load(self, lecture_id):

        path = self.metadata_path(

            lecture_id

        )

        if not path.exists():

            raise FileNotFoundError(

                f"Metadata not found : {lecture_id}"

            )

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    # =====================================================
    # Save Metadata
    # =====================================================

    def save(

        self,

        lecture_id,

        metadata

    ):

        metadata["lecture"]["last_updated"] = (

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

        with open(

            self.metadata_path(

                lecture_id

            ),

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                metadata,

                f,

                indent=4,

                ensure_ascii=False

            )

    # =====================================================
    # Update Pipeline
    # =====================================================

    def update_pipeline(

        self,

        lecture_id,

        **kwargs

    ):

        metadata = self.load(

            lecture_id

        )

        metadata["pipeline"].update(

            kwargs

        )

        self.save(

            lecture_id,

            metadata

        )

    # =====================================================
    # Update Files
    # =====================================================

    def update_files(

        self,

        lecture_id,

        **kwargs

    ):

        metadata = self.load(

            lecture_id

        )

        metadata["files"].update(

            kwargs

        )

        self.save(

            lecture_id,

            metadata

        )

    # =====================================================
    # Update Statistics
    # =====================================================

    def update_statistics(

        self,

        lecture_id,

        **kwargs

    ):

        metadata = self.load(

            lecture_id

        )

        metadata["statistics"].update(

            kwargs

        )

        self.save(

            lecture_id,

            metadata

        )

    # =====================================================
    # Update Models
    # =====================================================

    def update_models(

        self,

        lecture_id,

        **kwargs

    ):

        metadata = self.load(

            lecture_id

        )

        metadata["models"].update(

            kwargs

        )

        self.save(

            lecture_id,

            metadata

        )

    # =====================================================
    # Update Processing
    # =====================================================

    def update_processing(

        self,

        lecture_id,

        **kwargs

    ):

        metadata = self.load(

            lecture_id

        )

        metadata["processing"].update(

            kwargs

        )

        self.save(

            lecture_id,

            metadata

        )

    # =====================================================
    # Update Features
    # =====================================================

    def update_features(

        self,

        lecture_id,

        **kwargs

    ):

        metadata = self.load(

            lecture_id

        )

        metadata["features"].update(

            kwargs

        )

        self.save(

            lecture_id,

            metadata

        )

    # =====================================================
    # Update Exports
    # =====================================================

    def update_exports(

        self,

        lecture_id,

        **kwargs

    ):

        metadata = self.load(

            lecture_id

        )

        metadata["exports"].update(

            kwargs

        )

        self.save(

            lecture_id,

            metadata
        )