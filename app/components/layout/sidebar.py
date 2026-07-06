"""
=========================================================
AI Lecture Assistant
Sidebar Component
=========================================================

Responsibilities
----------------
1. Render Application Navigation
2. Update Selected Page
"""

import streamlit as st

from app.config.settings import APP_NAME, APP_VERSION
from state.session_manager import SessionManager


class Sidebar:

    from app.config.settings import (
        APP_VERSION,
        APP_NAME
    )

    # =====================================================
    # Navigation Items
    # =====================================================

    NAVIGATION = [

        ("🏠", "Dashboard"),

        ("📤", "Upload"),

        ("📝", "Summary"),

        ("📒", "Notes"),

        ("🧠", "Quiz"),

        ("💬", "Chat"),

        ("📊", "Metadata"),

        ("⚙️", "Settings")

    ]

    # =====================================================
    # Render
    # =====================================================

    @classmethod
    def render(cls):

        with st.sidebar:

            st.title("🎓 AI Lecture Assistant")

            st.divider()

            current_page = SessionManager.get(

                "selected_page",

                "Dashboard"

            )

            pages = [

                page

                for _, page in cls.NAVIGATION

            ]

            selected = st.radio(

                "Navigation",

                options=pages,

                index=pages.index(current_page),

                label_visibility="collapsed"

            )

            SessionManager.set(

                "selected_page",

                selected

            )

            st.divider()

            lecture = SessionManager.get_lecture()

            if lecture["lecture_name"]:

                st.caption("Current Lecture")

                st.success(

                    lecture["lecture_name"]

                )

            else:

                st.caption(

                    "No lecture selected."

                )

            st.divider()

            st.caption("AI Lecture Assistant")

            st.caption("Version 1.0.0")

            st.title(f"🎓 {APP_NAME}")



            st.caption(f"Version {APP_VERSION}")

            return selected