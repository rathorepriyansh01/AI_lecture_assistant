"""
=========================================================
AI Lecture Assistant
Summary Page
Production Version
=========================================================

Responsibilities
----------------
1. Initialize Session
2. Render Topbar
3. Render Summary Card
"""

import streamlit as st

from state.session_manager import SessionManager
from components.layout.topbar import Topbar
from components.cards.summary_card import SummaryCard


class SummaryPage:

    def __init__(self):

        self.card = SummaryCard()

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

page = SummaryPage()

page.render()