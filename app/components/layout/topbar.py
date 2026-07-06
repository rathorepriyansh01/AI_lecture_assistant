"""
=========================================================
AI Lecture Assistant
Topbar Component
=========================================================

Responsibilities
----------------
1. Render Application Header
2. Display Current Lecture
3. Display Backend Status
"""

import streamlit as st

from app.config.settings import (
    APP_NAME,
    APP_VERSION
)

from state.session_manager import SessionManager


class Topbar:

    # =====================================================
    # Render
    # =====================================================

    @classmethod
    def render(cls):

        col1, col2 = st.columns(

            [8, 2]

        )

        # ---------------------------------------------
        # Left Section
        # ---------------------------------------------

        with col1:

            st.title(f"🎓 {APP_NAME}")

            lecture = SessionManager.get_lecture()

            if lecture["lecture_name"]:

                st.caption(

                    f"Current Lecture : {lecture['lecture_name']}"

                )

            else:

                st.caption(

                    "No Lecture Selected"

                )

        # ---------------------------------------------
        # Right Section
        # ---------------------------------------------

        with col2:

            backend_status = SessionManager.get(

                "backend_status"

            )

            if backend_status:

                st.success("Backend Online")

            else:

                st.warning("Backend Offline")

            st.caption(

                f"Version {APP_VERSION}"

            )

        st.divider()