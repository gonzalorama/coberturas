import os
import uuid
from langchain_community.document_loaders import PyPDFLoader
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions
from typing import List, Dict
from chromadb import PersistentClient


class CompanyDocumentLoader:
    def __init__(self, root_path: str):
        self.root_path = root_path

    def load_documents(self) -> Dict[str, List[Dict]]:
        company_documents = {}
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)

        for company_name in os.listdir(self.root_path):
            company_path = os.path.join(self.root_path, company_name)

            if os.path.isdir(company_path):
                documents = []

                for filename in os.listdir(company_path):
                    if filename.endswith(".pdf"):
                        file_path = os.path.join(company_path, filename)
                        loader = PyPDFLoader(file_path)
                        chunks = text_splitter.split_documents(loader.load())
                        documents.extend(chunks)
                company_documents[company_name] = documents

        return company_documents

class CompanyDocumentIndexer:
    def __init__(self):
        self.client = PersistentClient()
        self.embedding_function = OpenAIEmbeddingFunction(
            api_key=os.environ.get('OPENAI_API_KEY'), 
            model_name='text-embedding-3-small'
            )

    def index_all_company_documents(self, root_path):
        loader = CompanyDocumentLoader(root_path)
        company_documents = loader.load_documents()
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-mpnet-base-v2")

        for company_name, documents in company_documents.items():
            docs_text = [self.process_doc_for_openai(doc) for doc in documents]
            collection = self.client.get_or_create_collection(
                name=company_name,
                embedding_function=sentence_transformer_ef
                )
            if(len(docs_text) == 0):
                continue
            collection.add(
                documents=docs_text, 
                ids=[f"{uuid.uuid4()}" for _ in range(len(docs_text))]
            )

    def process_doc_for_openai(self, doc):
        doc = doc.page_content.encode('utf-8', errors='replace').decode('utf-8')
        doc = doc.replace("\n", " ").replace('  ', ' ')
        return doc