import streamlit as st
from pathlib import Path

# Page header
container = st.container()
container.subheader("SciQuire app: under the hood", divider="red")
container.image(r"assets\visual.webp", width=800)

# read markdown content
md_path = Path("src/README_SciQuire.md")
content = md_path.read_text(encoding="utf-8")

# display markdown
container.markdown(content, unsafe_allow_html=True)