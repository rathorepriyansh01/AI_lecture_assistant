"""
=========================================================
AI Lecture Assistant
Base Card
Production Version
=========================================================

Reusable Card Component
"""

import streamlit as st


class BaseCard:

    # =====================================================
    # Start Card
    # =====================================================

    @staticmethod
    def start(
        title: str,
        icon: str = ""
    ):

        st.markdown("---")

        if icon:

            st.subheader(
                f"{icon} {title}"
            )

        else:

            st.subheader(
                title
            )

    # =====================================================
    # End Card
    # =====================================================

    @staticmethod
    def end():

        st.write("")

    # =====================================================
    # Success
    # =====================================================

    @staticmethod
    def success(message: str):

        st.success(message)

    # =====================================================
    # Error
    # =====================================================

    @staticmethod
    def error(message: str):

        st.error(message)

    # =====================================================
    # Warning
    # =====================================================

    @staticmethod
    def warning(message: str):

        st.warning(message)

    # =====================================================
    # Info
    # =====================================================

    @staticmethod
    def info(message: str):

        st.info(message)

    # =====================================================
    # Empty
    # =====================================================

    @staticmethod
    def empty(
        message: str = "No Data Available."
    ):

        st.info(message)