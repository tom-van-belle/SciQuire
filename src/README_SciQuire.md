#### Flow of the app:
- Scientist asks initial question (in natural language).
- The question is translated to PubMed query language via LLM.
- PubMed API is used to search and fetch relevant abstracts.
- Vector embeddings are generated from the abstracts and stored in a vector DB.
- Scientist’s original question is answered, using RAG. Scientist can then have follow up questions using the chat interface.

#### Technical walk-through (concise)
##### Startup:
- App renders header, sidebar info and the main input.
- Session initialization ensures singletons are in st.session_state: PubMedAbstractRetriever, LocalJSONStore, ChromaDbRag, ChatAgent, and session lists.

##### Phase 1 (One-shot question -> RAG answer):
- User types a question and clicks "Get abstracts & quick answer".
- The app fetches abstracts via pubmed_client.get_abstract_data.
- If abstracts are found:
- Save the dataset (LocalJSONStore.save_dataset) -> returns query_id.
- Create documents and build a Chroma vector index for that query.
- Retrieve nearest documents via chat_agent.retrieve_documents.
- Run the QA chain (qa_template | llm). The chain returns resp.content.
- The response is added into chat_agent.history and rendered via chat_agent.render_messages().
- The answer is persisted with data_repository.store_answer(query_id, resp.content).

##### Phase 2 (Chat with saved abstracts):
- User selects a saved query from a selectbox.
- App loads initial answer (if any) from data_repository.get_answer and displays it (once per session).
- Vector index for the selected query is loaded.
- If user switches query, chat history and session messages are reset.
- Existing messages from st.session_state.messages are rendered.
- On new prompt (st.chat_input), the user message is appended and shown.
- Within an assistant bubble, chat_agent.start_conversation is called (it returns the assistant text).
- The assistant text is rendered and stored in st.session_state.messages.

#### Inputs / Outputs / Data flow
##### Inputs:
- User text input (scientific question and chat prompts).
- External: PubMed via metapub.PubMedFetcher, LLM and embeddings providers (configured in components/llm.py and embeddings.py).
- API keys stored in .env or secrets.toml.
##### Outputs:
- UI content: quick answer and chat messages.
- Local files under RAG_Chatbot/backend/data/<query_id>/: abstracts.json, query_details.json, answer.txt.
- Vector index persisted in chromadb_storage.

#### Repo structure of this tool:
- RAG_Chatbot/
  - app.py
  - backend/
    - abstract_retrieval/
      - interface.py
      - pubmed_retriever.py
      - pubmed_query_simplification.py
    - data_repository/
      - interface.py
      - local_data_store.py
      - models.py
    - rag_pipeline/
      - interface.py
      - chromadb_rag.py
      - embeddings.py
    - data/
      - ...
    - chromadb_storage/
      - ...
  - components/
    - chat_utils.py
    - llm.py
    - prompts.py
  - tests/
    - test_chat_utils.py
    - test_pubmed_fetch.py
    - test_rag_pipeline.py
- assets/
  - ...
- environment/
  - requirements.txt

#### Source material:

❤️ Credits to Simona Barankova for the [pubmed-rag-screener GitHub repo](https://github.com/milieere/pubmed-rag-screener)
Key components of the abstract retrieval, vector embedding, and RAG pipeline design in this project are adapted from her implementation.

Part 1: Set up the Streamlit app with chatbot interface.
https://medium.com/@milieere/build-a-rag-based-scientific-chatbot-with-langchain-streamlit-pubmed-part-1-set-up-streamlit-37550b44b266


Part 2: LLM-aided retrieval of relevant scientific abstracts via PubMed API using natural language
https://blog.gopenai.com/llm-aided-retrieval-of-relevant-scientific-abstracts-via-pubmed-api-using-natural-language-part2-9e10f78575e6

Part 3: Setting up the backend — Create vector embeddings from the retrieved scientific abstracts and store them in a vector store
https://blog.gopenai.com/build-a-rag-based-scientific-chatbot-with-langchain-streamlit-pubmed-part-3-create-vector-1e5e401e72e6

Part 4: Put it all together via RAG— chat with scientific abstracts
https://blog.gopenai.com/build-a-rag-based-scientific-chatbot-with-langchain-streamlit-pubmed-part-4-put-it-all-ba7bbf706bbd