"""
=========================================================
AI Lecture Assistant
Notes Page
Production Version
=========================================================

Responsibilities
----------------
1. Initialize Session
2. Render Topbar
3. Render Notes Card
"""

from state.session_manager import SessionManager

from components.layout.topbar import Topbar
from components.cards.notes_card import NotesCard


class NotesPage:

    def __init__(self):

        self.card = NotesCard()

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

page = NotesPage()

page.render()