"""
=========================================================
AI Lecture Assistant
Statistics Card
=========================================================

Responsibilities
----------------
1. Display Lecture Statistics
"""

import streamlit as st


class StatisticsCard:

    # =====================================================
    # Render
    # =====================================================

    @classmethod
    def render(
        cls,
        statistics
    ):

        st.subheader("📊 Lecture Statistics")

        if not statistics:

            st.info(

                "Statistics not available."

            )

            return

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Duration",

                f"{statistics.get('video_duration', 0)} sec"

            )

            st.metric(

                "Language",

                statistics.get(

                    "language",

                    "-"

                )

            )

        with col2:

            st.metric(

                "Chunks",

                statistics.get(

                    "total_chunks",

                    0

                )

            )

            st.metric(

                "Words",

                statistics.get(

                    "total_words",

                    0

                )

            )

        with col3:

            st.metric(

                "Characters",

                statistics.get(

                    "total_characters",

                    0

                )

            )

            st.metric(

                "Audio",

                f"{statistics.get('audio_duration',0)} sec"

            )