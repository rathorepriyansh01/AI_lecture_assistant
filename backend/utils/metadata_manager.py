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
import shutil
from config.settings import LECTURES_DIR


class MetadataManager:

    def __init__(self):

        self.lectures_dir = Path(LECTURES_DIR)

    
    def health_check(self):

        return {

        "status": "healthy"

    }

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


    from pathlib import Path

    from config.settings import LECTURES_DIR


    def delete_lecture(
        self,
        lecture_id
    ):

        lecture_path = Path(LECTURES_DIR) / lecture_id

        if not lecture_path.exists():

            raise FileNotFoundError(
                f"Lecture not found : {lecture_id}"
            )

        shutil.rmtree(lecture_path)

        return {
            "success": True,
            "message": "Lecture deleted successfully.",
            "lecture_id": lecture_id
        }
    
    # =====================================================
    # List Lectures
    # =====================================================

    def list_lectures(self):

        lectures = []

        for lecture_folder in self.lectures_dir.iterdir():

            if not lecture_folder.is_dir():

                continue

            metadata_path = lecture_folder / "metadata.json"

            if not metadata_path.exists():

                continue

            try:

                with open(

                    metadata_path,

                    "r",

                    encoding="utf-8"

                ) as f:

                    metadata = json.load(f)

                lecture = metadata.get(

                    "lecture",

                    {}

                )

                statistics = metadata.get(

                    "statistics",

                    {}

                )

                pipeline = metadata.get(

                    "pipeline",

                    {}

                )

                lectures.append({

                    "lecture_id": lecture.get(

                        "lecture_id"

                    ),

                    "lecture_name": lecture.get(

                        "lecture_name"

                    ),

                    "uploaded_at": lecture.get(

                        "uploaded_at"

                    ),

                    "last_updated": lecture.get(

                        "last_updated"

                    ),

                    "language": statistics.get(

                        "language"

                    ),

                    "total_chunks": statistics.get(

                        "total_chunks"

                    ),

                    "ready_for_chat": pipeline.get(

                        "ready_for_chat",

                        False

                    )

                })

            except Exception:

                continue

        lectures.sort(

            key=lambda x: x["uploaded_at"],

            reverse=True

        )

        return lectures