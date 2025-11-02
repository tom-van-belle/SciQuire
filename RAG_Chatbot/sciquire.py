# app.py

import streamlit as st
from metapub import PubMedFetcher

from RAG_Chatbot.components.llm import llm
from RAG_Chatbot.components.chat_utils import ChatAgent
from RAG_Chatbot.components.chat_prompts import chat_prompt_template, qa_template
from RAG_Chatbot.components.layout_extensions import render_app_info
from RAG_Chatbot.backend.abstract_retrieval.pubmed_retriever import PubMedAbstractRetriever
from RAG_Chatbot.backend.data_repository.local_storage import LocalJSONStore
from RAG_Chatbot.backend.rag_pipeline.chromadb_rag import ChromaDbRag
from RAG_Chatbot.backend.rag_pipeline.embeddings import embeddings

# ---------- LAYOUT ----------
st.markdown("#### SciQuire: Chat with PubMed")
render_app_info()

placeholder = "Type your scientific question here."
scientist_question = st.text_input(
    "Type your scientific question here:",
    placeholder,
    label_visibility="hidden",
)

get_articles = st.button("Get abstracts & quick answer")

# ---------- SESSION INIT ----------
if "pubmed_client" not in st.session_state:
    st.session_state.pubmed_client = PubMedAbstractRetriever(PubMedFetcher())
if "data_repository" not in st.session_state:
    st.session_state.data_repository = LocalJSONStore(storage_folder_path="RAG_Chatbot/backend/data")
if "rag_client" not in st.session_state:
    st.session_state.rag_client = ChromaDbRag(
        persist_directory="RAG_Chatbot/backend/chromadb_storage", embeddings=embeddings
    )
if "chat_agent" not in st.session_state:
    st.session_state.chat_agent = ChatAgent(prompt=chat_prompt_template, llm=llm)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prev_selected_query" not in st.session_state:
    st.session_state.prev_selected_query = None

pubmed_client = st.session_state.pubmed_client
data_repository = st.session_state.data_repository
rag_client = st.session_state.rag_client
chat_agent = st.session_state.chat_agent
# SIDEBAR INFO
st.sidebar.markdown("##### SciQuire is using the following models:")
st.sidebar.caption("###### LLM model:")
st.sidebar.caption(f"{llm.model_name} (from Groq)")
st.sidebar.caption("###### Embeddings model:")
st.sidebar.caption(f"{embeddings.model} ({embeddings.provider})")
st.sidebar.write("---")

# ---------- PHASE 1: ASK A QUESTION ----------
if get_articles and scientist_question and scientist_question != placeholder:
    with st.spinner("Fetching abstracts and generating answer..."):
        retrieved_abstracts = pubmed_client.get_abstract_data(scientist_question)
        st.write(len(retrieved_abstracts), " abstracts retrieved from PubMed.")
        if not retrieved_abstracts:
            st.warning("No abstracts found.")
        else:
            query_id = data_repository.save_dataset(retrieved_abstracts, scientist_question)
            documents = data_repository.create_document_list(retrieved_abstracts)
            rag_client.create_vector_index_for_user_query(documents, query_id)

            vector_index = rag_client.get_vector_index_by_user_query(query_id)
            retrieved_docs = chat_agent.retrieve_documents(vector_index, scientist_question)
            chain = qa_template | llm
            
            st.markdown(f"##### Answer to your question: '{scientist_question}'")
            resp = chain.invoke(
                {"question": scientist_question, "retrieved_abstracts": retrieved_docs}
            )
            # Persist response to chat history
            chat_agent.history.add_ai_message(resp.content)
            chat_agent.render_messages()
            # Persist response to file 'query_answer.json' in the query folder
            data_repository.store_answer(query_id, resp.content)

# ---------- PHASE 2: CHAT WITH ABSTRACTS ----------

query_options = data_repository.get_list_of_queries()
if query_options:
    st.markdown("#### Chat with the abstracts")
    selected_query = st.selectbox(
        "Select a past query", options=list(query_options.values()), key="selected_query"
    )

    if selected_query:
        selected_query_id = next(k for k, v in query_options.items() if v == selected_query)
        # Display response content to the selected query
        initial_response = data_repository.get_answer(selected_query_id)
        abstract_count = data_repository.get_abstracts_count(selected_query_id)
        st.caption(f"###### Initial response from SciQuire (based on {abstract_count} abstracts retrieved from PubMed):")
        
        #st.caption(initial_response)
        if initial_response and not st.session_state.messages:
            st.chat_message("assistant").markdown(initial_response)
            st.session_state.messages.append({"role": "assistant", "content": initial_response})

        with st.spinner("Loading vector index of selected query..."):
            vector_index = rag_client.get_vector_index_by_user_query(selected_query_id)

        # Reset chat history if user switches topic
        if st.session_state.prev_selected_query != selected_query:
            st.session_state.messages = []
            chat_agent.reset_history()
        st.session_state.prev_selected_query = selected_query

        # Display existing messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # User sends new message
        if prompt := st.chat_input("Ask a follow-up question about the abstracts..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = chat_agent.start_conversation(vector_index, selected_query, prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
