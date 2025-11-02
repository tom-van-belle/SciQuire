import streamlit as st

# Page header
container = st.container()
col1, col2 = container.columns([1, 5])  # Adjust proportions of columns
col1.image(r"assets\book-brain-logo.jpg", width=100)
col2.subheader("SciQuire app: under the hood", divider="red")


# ---------- LAYOUT ----------
col_info, col_answer = st.columns([1, 5])
col_answer.markdown("🚧 WORK IN PROGRESS 🚧")
col_answer.image(r"assets\visual.webp", width=800)