from langchain.embeddings import OpenAIEmbeddings
from chromadb import Client
from chromadb.config import Settings
import openai
import os

class CompanyDocumentRetriever:
    def __init__(self, chroma_url):
        self.client = Client(Settings(chroma_url))
        self.embedding_model = OpenAIEmbeddings()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def retrieve_documents(self, company_name, query):
        query_vector = self.embedding_model.encode(query)
        collection = self.client.get_collection(company_name)
        results = collection.query(query_vector, n_results=5)
        return results
    
    def generate_answer(self, company_name, query):
        documents = self.retrieve_documents(company_name, query)
        context = "\n\n".join([doc['text'] for doc in documents])
        
        response = openai.Completion.create(
            engine="gpt-4o",
            prompt=f"Contexto: {context}\n\nPregunta: {query}\n\nRespuesta:",
            max_tokens=250
        )
        
        return response.choices[0].text.strip()