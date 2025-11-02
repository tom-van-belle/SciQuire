## Tool 1: A RAG-based scientific chatbot using LangChain, Steamlit and PubMed.

![image](https://github.com/user-attachments/assets/bc276c7b-dead-47f7-826b-a5409a575c32)

#### Flow of the tool:
- Streamlit interface
- Start conversation
  ├─ Display (historic) messages
  ├─ Receive input and feed into prompt (containing system message and a placeholder for user question).
  ├─ Output of prompt is input for llm (define and load model with API key) --> chain as a RunnableWithMessageHistory


- PubMed API to retrieve abstracts
  ├─ Pydantic library for data models
  ├─ Interface module to decouple Abstract Retriever client from its concrete implementation pubmed_retriever (to make it scalable to other sources)
  ├─ Enhancement of PubMed query via LLM (to simplify the user input from verbose language to simplified query)

- Naive RAG approach
  ├─ Persisting the data: store retrieved abstracts in local file system, in JSON files (subfolder per query_ID, containing abstracts.json with list of ScientificAbstracts*, and query_details.json with UserQueryRecord* (*: based on pydantic base models)) plus index.json with list of all queries
  ├─ Creating vector embeddings from the retrieved abstracts (here with mistral AI)
  ├─ Storing the vector embeddings in a vector store of your choice (here implementation using ChromaDB).

- Putting it all together
  ├─ Instantiate PubMedAbstractRetriever, LocalJSONStore, ChromaDbRag, and ChatAgent.
  ├─ 2 types of prompts: QA prompt for Q&A, and ChatBot to chat with the abstracts 

#### Source material:

Credits to Simona Barankova for the ![pubmed-rag-screener GitHub repo](https://github.com/milieere/pubmed-rag-screener) 

Part 1: Set up the Streamlit app with chatbot interface.
https://medium.com/@milieere/build-a-rag-based-scientific-chatbot-with-langchain-streamlit-pubmed-part-1-set-up-streamlit-37550b44b266


Part 2: LLM-aided retrieval of relevant scientific abstracts via PubMed API using natural language
https://blog.gopenai.com/llm-aided-retrieval-of-relevant-scientific-abstracts-via-pubmed-api-using-natural-language-part2-9e10f78575e6

Part 3: Setting up the backend — Create vector embeddings from the retrieved scientific abstracts and store them in a vector store
https://blog.gopenai.com/build-a-rag-based-scientific-chatbot-with-langchain-streamlit-pubmed-part-3-create-vector-1e5e401e72e6

Part 4: Put it all together via RAG— chat with scientific abstracts
https://blog.gopenai.com/build-a-rag-based-scientific-chatbot-with-langchain-streamlit-pubmed-part-4-put-it-all-ba7bbf706bbd

#### Repo structure of this tool:
.
├── app
│   ├── app.py
│   ├── backend
│   │  ├── abstract_retrieval
│   │  │   ├── interface.py
│   │  │   ├── pubmed_retriever.py
│   │  │   └── pubmed_query_simplification.py
│   │  ├── data_repository
│   │  │   ├── interface.py
│   │  │   ├── local_data_store.py
│   │  │   └── models.py
│   │  └── rag_pipeline
│   │      ├── interface.py
│   │      ├── chromadb_rag.py
│   │      └── embeddings.py
│   ├── components
│   │   ├── chat_utils.py
│   │   ├── llm.py
│   │   └── prompts.py
│   └── tests
│       └── test_chat_utils.py
├── assets
│   └── pubmed-screener-logo.jpg
└── environment
    └── requirements.txt

Where to look next in the codebase
----------------------------------
- `RAG_Chatbot/components/chat_utils.py` — chat orchestration and the ChatAgent implementation.
- `RAG_Chatbot/backend/rag_pipeline/` — RAG pipeline, embeddings and vector store adapter.
- `RAG_Chatbot/backend/data_repository/` — local JSON store and models.
- `RAG_Chatbot/components/llm.py` — where the LLM Runnable is configured.