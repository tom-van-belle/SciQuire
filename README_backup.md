# Welcome to the repo of SciQuire, a proof-of-concept scientific ChatBot!

<p align="center">
  <img src="assets/book-brain-logo.jpg" width="500" alt="Biomedical Abstract Screener">
</p>

- This project features the scientific chatbot SciQuire, an AI-powered insight generator using biomedical abstracts from PubMed.
- When you ask a question, the app will retrieve relevant abstracts from PubMed and generate insights based on them.
- Next you can ask follow-up questions to refine the insights, i.e. you can chat with the downloaded abstracts

### What you'll need to get started 
- The app uses an LLM model (for ...) and an embedding model, and access via API keys and credentials.
- To run this project as it is, you will need access to the Kimi K2 0905 model from Moonshot AI (loaded from Groq) and mistral-embed embeddings model.
- Alternatively, you can switch the LLM to any other LLM model available via langchain interfaces (i.e. ChatGPT and embedding models available via OpenAI directly).
- To plug in your own LLM and embeddings, please modify the following files:
    - /app/components/llm.py to edit LLM
    - /backend/rag_pipeline/embeddings.py

### Environment variables
- Handle your environment variables (API keys and credentials) in a .env file and use python-dotenv to retrieve them. Example .env file (with AzureOpenAI variables) can look like this:

```
AZURE_OPENAI_API_KEY=<llm-api-key>
AZURE_OPENAI_DEPLOYMENT_NAME=<llm-deployment-name>
AZURE_ENDPOINT=<llm-api-endpoint>
API_VERSION=<llm-api-version>

AZURE_OPENAI_API_KEY_EMBEDDINGS=<embeddings-api-key>
AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDINGS=<embeddings-deployment-name>
AZURE_ENDPOINT_EMBEDDINGS=<embeddings-endpoint>
API_VERSION_EMBEDDINGS=<embeddings-api-version>
```

### Environment installation

In the project root directory, create virtual environment using venv, and install dependencies from environment/requirements.txt file:

```
python -m venv venv
source venv/bin/activate
pip install -r environment/requirements.txt
```

### Run application

- Run the streamlit application `streamlit run app.py`
- Navigate in your browser to `http://localhost:8501`
- Have fun!