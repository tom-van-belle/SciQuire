import os, getpass
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def _get_env(var: str):

    API_KEY = os.getenv(var)
    if API_KEY is None:
        API_KEY = getpass.getpass(f"{var}: ")
        
    print(f"{var} key loaded")
    return API_KEY

# Load API keys from environment variables or prompt for them
MISTRAL_API_KEY = _get_env("MISTRAL_API_KEY")

embeddings = MistralAIEmbeddings(
    provider="mistralai",
    model="mistral-embed",
    api_key=MISTRAL_API_KEY,
)
