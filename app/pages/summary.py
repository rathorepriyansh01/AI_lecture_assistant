"""
=========================================================
AI Lecture Assistant
Summary Page
Production Version
=========================================================

Responsibilities
----------------
1. Render Summary Page
2. Generate Summary
3. Display Summary
"""

import streamlit as st

from components.layout.topbar import Topbar
from api.summary_api import SummaryAPI
from state.session_manager import SessionManager


class SummaryPage:

    def __init__(self):

        self.api = SummaryAPI()

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        Topbar.render()

        metadata = SessionManager.get("metadata")

        if not metadata:

            st.warning(

                "Please upload or select a lecture first."

            )

            return

        lecture = metadata.get("lecture", {})

        lecture_id = lecture.get("lecture_id")

        lecture_name = lecture.get("lecture_name")

        st.subheader("📝 Generate Summary")

        st.markdown(
            f"**Current Lecture :** `{lecture_name}`"
        )

        summary_type = st.selectbox(

            "Summary Type",

            [

                "short",

                "detailed",

                "bullet",

                "keypoints",

                "chapter"

            ]

        )

        use_cache = st.checkbox(

            "Use Cache",

            value=True

        )

        if st.button(

            "🚀 Generate Summary",

            use_container_width=True

        ):

            with st.spinner(

                "Generating Summary..."

            ):

                try:

                    response = self.api.generate(

                        lecture_id=lecture_id,

                        summary_type=summary_type,

                        use_cache=use_cache

                    )

                    data = response.get(

                        "data",

                        {}

                    )

                    st.success(

                        "Summary Generated Successfully."

                    )

                    st.markdown("---")

                    st.markdown(

                        data.get(

                            "summary",

                            "No Summary Generated."

                        )

                    )

                    statistics = data.get(

                        "statistics",

                        {}

                    )

                    if statistics:

                        st.markdown("---")

                        col1, col2 = st.columns(2)

                        with col1:

                            st.metric(

                                "Execution Time",

                                f"{statistics.get('execution_time',0)} sec"

                            )

                        with col2:

                            st.metric(

                                "Context Parts",

                                statistics.get(

                                    "parts",

                                    0

                                )

                            )

                except Exception as e:

                    st.error(

                        str(e)

                    )