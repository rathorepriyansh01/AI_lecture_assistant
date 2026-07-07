"""
=========================================================
AI Lecture Assistant
Home
Production Version
=========================================================

Application Entry Point
"""

import streamlit as st

from utils.theme import apply_theme
from state.session_manager import SessionManager


# =====================================================
# Initialize
# =====================================================

def initialize():

    apply_theme()

    SessionManager.initialize()


# =====================================================
# Main
# =====================================================

def main():

    st.set_page_config(

        page_title="AI Lecture Assistant",

        page_icon="🎓",

        layout="wide"

    )

    initialize()
    SessionManager.initialize()

    st.title("🎓 AI Lecture Assistant")

    st.markdown(
        """
        ## Welcome 👋

        AI Lecture Assistant helps you:

        - 📤 Upload lecture videos
        - 📝 Generate summaries
        - 📒 Create notes
        - 🧠 Generate quizzes
        - 💬 Chat with lectures
        - 📊 View lecture metadata

        ---
        ### 👈 Select a page from the sidebar to get started.
        """
    )


if __name__ == "__main__":

    main()