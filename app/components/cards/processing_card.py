"""
=========================================================
AI Lecture Assistant
Processing Card
Production Version
=========================================================

Displays Lecture Processing Pipeline.

Responsibilities
----------------
1. Display Processing Pipeline
2. Display Overall Progress
"""

import streamlit as st

from components.cards.base_card import BaseCard


class ProcessingCard:

    PIPELINE = [

        ("upload_completed", "📤 Upload"),

        ("audio_extracted", "🎵 Audio"),

        ("transcription_completed", "📝 Transcription"),

        ("chunking_completed", "✂️ Chunking"),

        ("embedding_completed", "🧠 Embeddings"),

        ("vector_db_completed", "🗂️ Vector Database"),

        ("ready_for_chat", "💬 Ready For Chat")

    ]

    # =====================================================
    # Render
    # =====================================================

    @classmethod
    def render(
        cls,
        pipeline
    ):

        BaseCard.start(

            "Processing Pipeline",

            "⚙️"

        )

        if not pipeline:

            BaseCard.empty(

                "Pipeline information not available."

            )

            BaseCard.end()

            return

        completed = 0

        total = len(cls.PIPELINE)

        progress = []

        for key, title in cls.PIPELINE:

            status = pipeline.get(

                key,

                False

            )

            if status:

                completed += 1

                progress.append(

                    f"✅ {title}"

                )

            else:

                progress.append(

                    f"⏳ {title}"

                )

        st.progress(

            completed / total

        )

        st.caption(

            f"{completed}/{total} stages completed"

        )

        col1, col2 = st.columns(2)

        midpoint = (len(progress) + 1) // 2

        with col1:

            for item in progress[:midpoint]:

                st.write(item)

        with col2:

            for item in progress[midpoint:]:

                st.write(item)

        BaseCard.end()