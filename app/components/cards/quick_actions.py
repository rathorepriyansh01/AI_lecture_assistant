"""
=========================================================
AI Lecture Assistant
Quick Actions Card
Production Version
=========================================================

Responsibilities
----------------
1. Display Dashboard Actions
2. Trigger Navigation Events
"""

import streamlit as st

from components.cards.base_card import BaseCard
from state.session_manager import SessionManager


class QuickActions:

    # =====================================================
    # Render
    # =====================================================

    @classmethod
    def render(cls):

        BaseCard.start(

            "Quick Actions",

            "⚡"

        )

        col1, col2, col3 = st.columns(3)

        # -------------------------------------------------
        # Row 1
        # -------------------------------------------------

        with col1:

            if st.button(

                "📝 Summary",

                use_container_width=True

            ):

                SessionManager.set(

                    "selected_page",

                    "Summary"

                )

                st.rerun()

        with col2:

            if st.button(

                "📒 Notes",

                use_container_width=True

            ):

                SessionManager.set(

                    "selected_page",

                    "Notes"

                )

                st.rerun()

        with col3:

            if st.button(

                "🧠 Quiz",

                use_container_width=True

            ):

                SessionManager.set(

                    "selected_page",

                    "Quiz"

                )

                st.rerun()

        st.write("")

        col1, col2, col3 = st.columns(3)

        # -------------------------------------------------
        # Row 2
        # -------------------------------------------------

        with col1:

            if st.button(

                "💬 Chat",

                use_container_width=True

            ):

                SessionManager.set(

                    "selected_page",

                    "Chat"

                )

                st.rerun()

        with col2:

            if st.button(

                "📊 Metadata",

                use_container_width=True

            ):

                SessionManager.set(

                    "selected_page",

                    "Metadata"

                )

                st.rerun()

        with col3:

            if st.button(

                "📤 Upload",

                use_container_width=True

            ):

                SessionManager.set(

                    "selected_page",

                    "Upload"

                )

                st.rerun()

        BaseCard.end()