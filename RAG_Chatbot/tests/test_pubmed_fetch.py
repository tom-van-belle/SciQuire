from metapub import PubMedFetcher
from backend.abstract_retrieval.pubmed_retriever import PubMedAbstractRetriever

pubmed_fetcher = PubMedFetcher()
abstract_retriever = PubMedAbstractRetriever(pubmed_fetcher)

# Retrieve abstracts without query simplification
scientist_question = "Has there been any significant progress in Alzheimer's disease treatment using monoclonal antibodies in the last five years?"
abstracts = abstract_retriever.get_abstract_data(scientist_question, simplify_query=False)

# Retrieve abstracts with query simplification (default behavior)
abstracts = abstract_retriever.get_abstract_data(scientist_question)