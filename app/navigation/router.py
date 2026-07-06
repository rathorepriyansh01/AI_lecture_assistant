"""
=========================================================
AI Lecture Assistant
Navigation Router
Production Version
=========================================================

Responsibilities
----------------
1. Register Pages
2. Handle Navigation
3. Render Active Page
"""

from state.session_manager import SessionManager

from pages.dashboard import Dashboard
from pages.upload import UploadPage

# Future Pages
from pages.summary import SummaryPage
# from app.pages.notes import NotesPage
# from app.pages.quiz import QuizPage
# from app.pages.chat import ChatPage
# from app.pages.metadata import MetadataPage


class AppRouter:

    def __init__(self):

        self.routes = {

            "Dashboard": Dashboard(),

            "Upload": UploadPage(),

            "Summary": SummaryPage(),
            # "Notes": NotesPage(),
            # "Quiz": QuizPage(),
            # "Chat": ChatPage(),
            # "Metadata": MetadataPage(),

        }

    # =====================================================
    # Current Page
    # =====================================================

    def current_page(self):

        return SessionManager.get(

            "selected_page",

            "Dashboard"

        )

    # =====================================================
    # Navigate
    # =====================================================

    def navigate(

        self,

        page

    ):

        SessionManager.set(

            "selected_page",

            page

        )

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        page = self.current_page()

        view = self.routes.get(page)

        if view is None:

            self.routes["Dashboard"].render()

            return

        view.render()