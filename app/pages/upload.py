"""
=========================================================
AI Lecture Assistant
Upload Page
Production Version
=========================================================

Responsibilities
----------------
1. Render Upload Page
2. Handle Upload Workflow
3. Update Session
4. Display Notifications
"""

import streamlit as st

from components.layout.topbar import Topbar
from components.cards.upload_card import UploadCard

from state.session_manager import SessionManager


class UploadPage:

    def __init__(self):

        self.upload = UploadCard()

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        st.write("STEP 1")

        Topbar.render()

        st.write("STEP 2")

        response = self.upload.render()

        st.write("STEP 3")


        response = self.upload.render()

        if response is None:

            return

        lecture = response["data"]["lecture"]

        SessionManager.set_lecture(

            lecture["lecture_id"],

            lecture["lecture_name"]

        )

        SessionManager.set(

            "metadata",

            response["data"]

        )

        st.success(

            "Lecture uploaded successfully."

        )

        st.balloons()

        if st.button(

            "🏠 Go To Dashboard",

            use_container_width=True

        ):

            SessionManager.set(

                "selected_page",

                "Dashboard"

            )

            st.rerun()
# import streamlit as st

# st.write("UPLOAD PAGE STARTED")

# from components.layout.topbar import Topbar
# st.write("TOPBAR IMPORTED")

# from components.cards.upload_card import UploadCard
# st.write("UPLOAD CARD IMPORTED")

# from state.session_manager import SessionManager
# st.write("SESSION IMPORTED")


# class UploadPage:

#     def __init__(self):
#         self.upload = UploadCard()

#     def render(self):

#         st.write("RENDER START")

#         Topbar.render()

#         st.write("TOPBAR DONE")

#         response = self.upload.render()

#         st.write("UPLOAD DONE")