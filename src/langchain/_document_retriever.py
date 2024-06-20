from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
import openai
import os

class CompanyDocumentRetriever:
    def __init__(self):
        self.client = PersistentClient(
            path=os.environ.get('CHROMA_DB_PATH') 
        )
        self.embedding_model = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125",
            temperature=0.8,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def retrieve_documents(self, company_name, query):
        collection = self.client.get_collection(company_name)
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-mpnet-base-v2")
        vector = sentence_transformer_ef(query)
        results = collection.query(
            query_embeddings=vector, 
            n_results=5
        )
        return results['documents'][0]
    
    def generate_answer(self, company_name, query):
        documents = self.retrieve_documents(company_name, query)
        context = "\n\n".join([doc for doc in documents])
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Eres un experto asesor en seguros del hogar y debes contestar la pregunta con el contexto dado que se corresponde a los datos extraidos de la poliza.",
                ),
                ("human", "Contexto: {context}\n\nPregunta: {query}"),
            ]
        )
        llm_chain = prompt | self.llm
        print(context)
        return llm_chain.invoke(
            {
                "query": query,
                "context": context,
            }
        ).content
