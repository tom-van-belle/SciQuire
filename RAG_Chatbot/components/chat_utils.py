from typing import List
import streamlit as st
from langchain_core.documents.base import Document
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.base import Runnable
from langchain_core.runnables.utils import Output
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStore

class ChatAgent:
    def __init__(self, prompt: ChatPromptTemplate, llm: Runnable):
        """
        Initialize the ChatAgent.

        Args:
        - prompt (ChatPromptTemplate): The chat prompt template.
        - llm (Runnable): The language model runnable.
        """
        self.history = StreamlitChatMessageHistory(key="chat_history")
        self.llm = llm
        self.prompt = prompt
        self.chain = self.setup_chain()
    
    def reset_history(self) -> None:
        """
        Clean up chat history to start new chat session.
        """
        self.history.clear()

    def setup_chain(self) -> RunnableWithMessageHistory:
        """
        Set up the chain for the ChatAgent.

        Returns:
        - RunnableWithMessageHistory: The configured chain with message history.
        """
        chain = self.prompt | self.llm
        return RunnableWithMessageHistory(
            chain,
            lambda session_id: self.history,
            input_messages_key="question",
            history_messages_key="history",
        )

    def display_messages(self, selected_query: str) -> None:
        """
        Return the current chat history as a list of message dicts.

        This method does NOT perform any Streamlit rendering to avoid
        accidental nested `st.chat_message` calls. Callers that want to
        render the messages in the UI should call `render_messages()`.

        Args:
            selected_query: Optional query string used to seed the history
                when history is empty.

        Returns:
            List[dict]: Each dict contains keys 'role' and 'content'.
        """
        if len(self.history.messages) == 0 and selected_query:
            # Seed the history with a starter AI message for this query
            self.history.add_ai_message(f"Let's chat about your query: {selected_query}")

        return [{"role": msg.type, "content": msg.content} for msg in self.history.messages]

    def render_messages(self) -> None:
        """
        Render the current history to the Streamlit chat UI.

        Kept as a separate method to avoid creating UI components while
        already inside another `st.chat_message` context (which causes
        StreamlitAPIException for nested chat messages).
        """
        for msg in self.history.messages:
            st.chat_message(msg.type).write(msg.content)
    
    def format_retrieved_abstracts_for_prompt(self, documents: List[Document]) -> str:
        """
        Format retrieved documents in a string to be passed to LLM.
        """
        formatted_strings = []
        for doc in documents:
            formatted_str = f"ABSTRACT TITLE: {doc.metadata['title']}, ABSTRACT CONTENT: {doc.page_content}, ABSTRACT DOI: {doc.metadata['source'] if 'source' in doc.metadata.keys() else 'DOI missing..'}"
            formatted_strings.append(formatted_str)
        return "; ".join(formatted_strings)
    
    def get_answer_from_llm(self, question: str, retrieved_documents: List[Document]) -> Output:
        """
        Get response from LLM given user question and retrieved documents.
        """
        config = {"configurable": {"session_id": "any"}}
        return self.chain.invoke(
            {
                "question": question, 
                "retrieved_abstracts": retrieved_documents,
            }, config
        )
    
    def retrieve_documents(self, retriever: VectorStore, question: str, cut_off: int = 5) -> List[Document]:
        """
        Retrieve documents using similarity search 
        cut_off parameter controls how many results are retrieved (default is 5)
        """
        return retriever.similarity_search(question)[:cut_off]

    def start_conversation(
        self, retriever: VectorStore, selected_query: str, user_question: str
    ) -> str:
        """
        Given a user question, retrieve relevant documents from the retriever,
        call the LLM chain, and return the assistant's answer as a string.

        This method intentionally does NOT call Streamlit UI functions (like
        `st.chat_message`) so callers can control rendering and avoid nested
        chat message contexts.
        """
        if not user_question:
            return ""

        try:
            documents = self.retrieve_documents(retriever, user_question)
            # Pass Document list to the chain (the chain expects structured docs)
            response = self.get_answer_from_llm(user_question, documents)
            return response.content
        except Exception as e:
            # Return a helpful error string so the caller can display it.
            import traceback

            return f"Error getting response from LLM: {e}\n{traceback.format_exc()}"