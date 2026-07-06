"""
=========================================================
AI Lecture Assistant
Theme Manager
=========================================================

Handles

• Streamlit Page Configuration
• Global CSS
• Theme Loading
"""

from pathlib import Path

import streamlit as st

from app.config.settings import (

    APP_NAME,

    APP_VERSION

)


# =========================================================
# Page Config
# =========================================================

def configure_page():

    st.set_page_config(

        page_title=APP_NAME,

        page_icon="🎓",

        layout="wide",

        initial_sidebar_state="expanded"

    )


# =========================================================
# Load CSS
# =========================================================

def load_css():

    css_dir = (

        Path(__file__).resolve().parents[1]

        / "assets"

        / "css"

    )

    css_files = [

        "main.css",

        "dashboard.css",

        "chat.css",

        "cards.css"

    ]

    for css in css_files:

        file_path = css_dir / css

        if file_path.exists():

            with open(

                file_path,

                encoding="utf-8"

            ) as f:

                st.markdown(

                    f"<style>{f.read()}</style>",

                    unsafe_allow_html=True

                )


# =========================================================
# Header
# =========================================================

def render_header():

    col1, col2 = st.columns(

        [8, 2]

    )

    with col1:

        st.title(APP_NAME)

    with col2:

        st.caption(

            f"v{APP_VERSION}"

        )


# =========================================================
# Apply Theme
# =========================================================

def apply_theme():

    configure_page()

    load_css()