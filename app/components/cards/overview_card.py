"""
=========================================================
AI Lecture Assistant
Overview Card
Production Version
=========================================================

Displays lecture overview information.

Responsibilities
----------------
1. Display Lecture Information
2. Display Lecture Statistics
3. Display Current Status
"""

from datetime import datetime

import streamlit as st

from app.components.cards.base_card import BaseCard


class OverviewCard:

    # =====================================================
    # Render
    # =====================================================

    @classmethod
    def render(
        cls,
        metadata
    ):

        BaseCard.start(

            "Lecture Overview",

            "📚"

        )

        if not metadata:

            BaseCard.empty(

                "No lecture selected."

            )

            BaseCard.end()

            return

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

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # Left Column
        # -------------------------------------------------

        with col1:

            st.metric(

                "Lecture Name",

                lecture.get(

                    "lecture_name",

                    "-"

                )

            )

            st.metric(

                "Language",

                statistics.get(

                    "language",

                    "-"

                )

            )

            st.metric(

                "Duration",

                f"{statistics.get('video_duration',0)} sec"

            )

            st.metric(

                "Total Chunks",

                statistics.get(

                    "total_chunks",

                    0

                )

            )

        # -------------------------------------------------
        # Right Column
        # -------------------------------------------------

        with col2:

            st.metric(

                "Uploaded",

                lecture.get(

                    "uploaded_at",

                    "-"

                )

            )

            st.metric(

                "Last Updated",

                lecture.get(

                    "last_updated",

                    "-"

                )

            )

            st.metric(

                "Words",

                statistics.get(

                    "total_words",

                    0

                )

            )

            status = (

                "🟢 Ready"

                if pipeline.get(

                    "ready_for_chat",

                    False

                )

                else "🟡 Processing"

            )

            st.metric(

                "Status",

                status

            )

        BaseCard.end()