

from langchain.chat_models import init_chat_model
import streamlit as st
import os

# Load API keys securely from Streamlit secrets
os.environ["MISTRAL_API_KEY"] = st.secrets["api_keys"]["MISTRAL_API_KEY"]
os.environ["GROQ_API_KEY"] = st.secrets["api_keys"]["GROQ_API_KEY"]
os.environ["NCBI_API_KEY"] = st.secrets["api_keys"]["NCBI_API_KEY"]

# Define the llm
from langchain.chat_models import init_chat_model

llm = init_chat_model(model="moonshotai/kimi-k2-instruct-0905", model_provider="groq")
print("Kimi model loaded from Groq")