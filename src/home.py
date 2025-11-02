"""Home page shown when the user enters the application"""
import streamlit as st

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Home ..."):
        left_column, center_column,last_column = st.columns([1, 5, 1])
        with center_column:
            left_img_col, img_col, right_img_col = st.columns([1,2,1])
            with img_col:
                st.image(r"assets/Rosalind.jpg", width=160)
            st.subheader("Biomedical Research & Development Suite")
            
            st.write(
            """
            Welcome to **Rosalind**, a biomedical research and development suite.
            """
            )
            st.write(
            """
            This app is designed to assist researchers in their scientific inquiries.
            """
            )
            st.write(
            """
            SciQuire: a chatbot that can retrieve relevant abstracts from PubMed biomedical literature and get answers to your scientific questions.
            """
            )
            st.write(
                """
                Select an app from the sidebar to get started.
                """
            )

write()
