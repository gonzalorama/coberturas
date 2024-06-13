import os
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from typing import List, Dict
from chromadb import Client
from chromadb.config import Settings

class CompanyDocumentLoader:
    def __init__(self, root_path: str):
        self.root_path = root_path

    def load_documents(self) -> Dict[str, List[Dict]]:
        company_documents = {}

        for company_name in os.listdir(self.root_path):
            company_path = os.path.join(self.root_path, company_name)

            if os.path.isdir(company_path):
                documents = []

                for filename in os.listdir(company_path):
                    if filename.endswith(".pdf"):
                        file_path = os.path.join(company_path, filename)
                        loader = UnstructuredPDFLoader(file_path)
                        documents.extend(loader.load())
                company_documents[company_name] = documents

        return company_documents

class CompanyDocumentIndexer:
    def __init__(self, chroma_url):
        self.client = Client(Settings(chroma_url))
        self.embedding_model = OpenAIEmbeddings()

    def index_all_company_documents(self, root_path):
        loader = CompanyDocumentLoader(root_path)
        company_documents = loader.load_documents()

        for company_name, documents in company_documents.items():
            collection = self.client.get_or_create_collection(company_name)
            for doc in documents:
                vector = self.embedding_model.encode(doc['text'])
                collection.add(doc['id'], vector, doc['text'])