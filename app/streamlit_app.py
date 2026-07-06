"""
=========================================================
AI Lecture Assistant
Streamlit Entry Point
=========================================================

Application Bootstrap

Responsibilities
----------------
1. Configure Streamlit Page
2. Apply Global Theme
3. Initialize Session
4. Load Dashboard
"""

from utils.theme import (
    apply_theme
)

from state.session_manager import (
    SessionManager
)

from pages.dashboard import (
    show_dashboard
)


# =====================================================
# Initialize Application
# =====================================================

def initialize():

    apply_theme()

    SessionManager.initialize()


# =====================================================
# Main
# =====================================================

def main():

    initialize()

    show_dashboard()


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    main()