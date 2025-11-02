import streamlit as st
from pathlib import Path

# Page header
container = st.container()
container.subheader("SciQuire app: under the hood", divider="red")
container.image(r"assets\SciQuire_visual.png", width=800)


st.sidebar.markdown("""
---
<div style="text-align: left;">
    Built with ❤️ by <a href="https://www.linkedin.com/in/tom-van-belle/" target="_blank">Tom</a>
</div>
""", unsafe_allow_html=True)

# read markdown content
md_path = Path("src/README_SciQuire.md")
content = md_path.read_text(encoding="utf-8")

# display markdown
container.markdown(content, unsafe_allow_html=True)