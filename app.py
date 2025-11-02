import streamlit as st


home = st.Page("src/home.py", title="Home", icon="🏠")
sciquire = st.Page("RAG_Chatbot/sciquire.py", title="SciQuire: Chat with PubMed", icon="💬")
research_agent = st.Page("src/sciquire_technical.py", title="SciQuire: Technical explanations", icon="🤖")

pg = st.navigation([home, sciquire, research_agent])

st.set_page_config(page_title="SciQuire", layout="wide", page_icon=":microscope:")

pg.run()
