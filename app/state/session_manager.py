"""
=========================================================
AI Lecture Assistant
Session Manager
=========================================================

Centralized Streamlit Session State Manager.

Every page should use this manager instead of directly
accessing st.session_state.
"""

import streamlit as st


class SessionManager:

    # =====================================================
    # Initialize Session
    # =====================================================

    @staticmethod
    def initialize():

        defaults = {

            # -----------------------------------------
            # Lecture
            # -----------------------------------------

            "lecture_id": None,

            "lecture_name": None,

            "metadata": None,

            # -----------------------------------------
            # Generated Content
            # -----------------------------------------

            "summary": None,

            "notes": None,

            "quiz": None,

            # -----------------------------------------
            # Chat
            # -----------------------------------------

            "chat_history": [],

            # -----------------------------------------
            # UI
            # -----------------------------------------

            "selected_page": "Dashboard",

            "processing": False,

            "backend_status": None

        }

        for key, value in defaults.items():

            if key not in st.session_state:

                st.session_state[key] = value

    # =====================================================
    # Generic Setter
    # =====================================================

    @staticmethod
    def set(

        key,

        value

    ):

        st.session_state[key] = value

    # =====================================================
    # Generic Getter
    # =====================================================

    @staticmethod
    def get(

        key,

        default=None

    ):

        return st.session_state.get(

            key,

            default

        )

    # =====================================================
    # Current Lecture
    # =====================================================

    @staticmethod
    def set_lecture(

        lecture_id,

        lecture_name=None

    ):

        st.session_state.lecture_id = lecture_id

        st.session_state.lecture_name = lecture_name

    @staticmethod
    def get_lecture():

        return {

            "lecture_id": st.session_state.lecture_id,

            "lecture_name": st.session_state.lecture_name

        }

    # =====================================================
    # Chat
    # =====================================================

    @staticmethod
    def add_chat_message(

        role,

        content

    ):

        st.session_state.chat_history.append(

            {

                "role": role,

                "content": content

            }

        )

    @staticmethod
    def clear_chat():

        st.session_state.chat_history = []

    # =====================================================
    # Clear Generated Content
    # =====================================================

    @staticmethod
    def clear_outputs():

        st.session_state.summary = None

        st.session_state.notes = None

        st.session_state.quiz = None

        st.session_state.chat_history = []

    # =====================================================
    # Reset Everything
    # =====================================================

    @staticmethod
    def reset():

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        SessionManager.initialize()

    @staticmethod
    def navigate(page):

        SessionManager.set(

            "selected_page",

            page

        )