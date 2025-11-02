# SciQuire, a scientific ChatBot!

<p align="center">
  <img src="assets/book-brain-logo.jpg" width="500" alt="Biomedical Abstract Screener">
</p>

### Short summary
-------------------
SciQuire is a proof-of-concept small RAG (Retrieval-Augmented Generation) demo that lets you fetch PubMed abstracts for a scientific question and then chat with those abstracts using a conversational interface. The app is built with Streamlit and a lightweight RAG pipeline (ChromaDB for vector storage + an embeddings/LLM runnable). It stores datasets locally under `backend/data` and persists vector indices under `backend/chromadb_storage` for quick reuse.

### What you'll find in this repo
----------------------------------
- `RAG_Chatbot/` - main app code and backend components (retriever, data repository, RAG pipeline, chat UI).
- `streamlit_app.py` and `RAG_Chatbot/sciquire.py` - Streamlit entry points for running the app.
- `requirements.txt` - Python dependencies used by the project.
- `backend/data/` and `RAG_Chatbot/backend/data/` - sample/local datasets and storage folders.
- `assets/` - UI assets such as logo images.
- `RAG_Chatbot/tests/` - unit tests for some components.

### Prerequisites / what you need to get started
-------------------------------------------------
- Python 3.10+ (3.11/3.12 should work, but ensure dependencies are installed into a matching interpreter).
- A working internet connection for fetching PubMed data and contacting any LLM/embedding provider you configure.
- Recommended: create and use a virtual environment.

### Quick setup (Windows / PowerShell)
----------------------------------------
Open PowerShell in the project root (`c:\Users\tom_v\AI_projects\SciQuire`) and run:

```powershell
# create a venv (if you don't have one)
python -m venv .venv
# activate the venv
.\.venv\Scripts\Activate.ps1
# install dependencies
pip install -r environment/requirements.txt
```

### Configuration — where to place API keys and credentials
-------------------------------------------------------------
When running it as it is, the app deploys locally and reads configuration and secrets from the `.streamlit/secrets.toml file. When deploying to Streamlit Cloud, define secrets in its web UI instead. 

Local example:
```toml
# .streamlit/secrets.toml
MISTRAL_API_KEY = "REPLACE_WITH_YOUR_KEY"
GROQ_API_KEY = "REPLACE_WITH_YOUR_KEY"
NCBI_API_KEY = "REPLACE_WITH_YOUR_KEY"
# Other provider keys as needed (e.g. for other LLMs or embedding models)
```

Notes on secrets and safety
- Do NOT commit `.env` or `.streamlit/secrets.toml` with real API keys to source control. Add them to `.gitignore`.
- If you accidentally commit keys, rotate them at the provider immediately.


### Run application

- From a PowerShell prompt in the project root and with your virtualenv active: run the streamlit application `streamlit run app.py`
- This opens a local Streamlit server and a browser tab. Navigate in your browser to `http://localhost:8501`
- The UI has two main flows:
-- Enter a scientific question and click "Get abstracts & quick answer" — this fetches PubMed abstracts, stores them locally, builds a vector index, and returns a quick answer.
-- "Chat with the abstracts" — pick a saved query and start a follow-up chat around that dataset.
- Have fun!