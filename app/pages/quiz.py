"""
=========================================================
AI Lecture Assistant
Quiz Page
Production Version
=========================================================

Responsibilities
----------------
1. Initialize Session
2. Render Topbar
3. Render Quiz Card
"""

from state.session_manager import SessionManager

from components.layout.topbar import Topbar
from app.components.quiz.quiz_card import QuizCard


class QuizPage:

    def __init__(self):

        self.card = QuizCard()

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        SessionManager.initialize()

        Topbar.render()

        self.card.render()


# ==========================================================
# Streamlit Entry Point
# ==========================================================

page = QuizPage()

page.render()