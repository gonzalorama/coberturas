from src.langchain._document_retriever import CompanyDocumentRetriever
retriever = CompanyDocumentRetriever()
docs = retriever.retrieve_documents('occident', 'Cubre un tornado?')
