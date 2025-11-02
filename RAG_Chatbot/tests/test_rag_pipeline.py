from metapub import PubMedFetcher
from backend.rag_pipeline.embeddings import embeddings
from backend.abstract_retrieval.pubmed_retriever import PubMedAbstractRetriever
from backend.data_repository.local_storage import LocalJSONStore
from backend.rag_pipeline.chromadb_rag import ChromaDbRag

query = "Does abamectin cause cancer?"

# Step 1: Use PubMedAbstractRetriever to get abstract data for a query "Does abamectin cause cancer?"
pubmed_fetcher = PubMedFetcher()
abstract_retriever = PubMedAbstractRetriever(pubmed_fetcher)
abstracts = abstract_retriever.get_abstract_data(query)

# Step 2: Use the retrieved data with LocalJSONStorage to persist them in local storage
storage_folder_path = "backend/data"
store = LocalJSONStore(storage_folder_path)
query_id = store.save_dataset(abstracts, query)

# Step 3: Use ChromDBRAGWorkflow to create a vector index using the list of documents created via LocalJSONStorage
persist_directory = "backend/chromadb_storage"
rag_workflow = ChromaDbRag(persist_directory, embeddings)
documents = store.read_documents(query_id)
vector_index = rag_workflow.create_vector_index_for_user_query(documents, query_id)

# Run similarity search on newly created index, using the original user query: 
print(vector_index.similarity_search(query))