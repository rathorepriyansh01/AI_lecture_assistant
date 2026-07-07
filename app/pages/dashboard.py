# """
# =========================================================
# AI Lecture Assistant
# Dashboard
# Production Version
# =========================================================

# Responsibilities
# ----------------
# 1. Render Dashboard Layout
# 2. Assemble Dashboard Components
# """

import streamlit as st

from components.layout.topbar import Topbar
from components.common.lecture_selector import LectureSelector

from components.cards.overview_card import OverviewCard
from components.cards.processing_card import ProcessingCard
from components.cards.quick_actions import QuickActions

from state.session_manager import SessionManager


class Dashboard:

    def __init__(self):

        self.selector = LectureSelector()

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        # ---------------------------------------------
        # Header
        # ---------------------------------------------

        Topbar.render()

        # ---------------------------------------------
        # Lecture Selector
        # ---------------------------------------------

        self.selector.render()

        metadata = SessionManager.get(

            "metadata"

        )

        if not metadata:

            st.info(

                "Please upload or select a lecture."

            )

            return

        # ---------------------------------------------
        # Overview
        # ---------------------------------------------

        OverviewCard.render(

            metadata

        )

        # ---------------------------------------------
        # Processing Pipeline
        # ---------------------------------------------

        ProcessingCard.render(

            metadata.get(

                "pipeline",

                {}

            )

        )

        # ---------------------------------------------
        # Quick Actions
        # ---------------------------------------------

        QuickActions.render()

page = Dashboard()
page.render()
