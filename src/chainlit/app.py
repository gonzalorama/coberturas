import chainlit as cl
from src.langchain.company_document_retriever import CompanyDocumentRetriever
from src.api.openai import OpenAI

OpenAI()

document_retriever = CompanyDocumentRetriever("your_chroma_db_url")
companies = ["Allianz", "Generali", "Liberty", "Mapfre", "Mutua Madrileña", "Occident", "Santa Lucía", "Zurich"]

@cl.app
def main():
    cl.page("Asistente de coberturas de seguros del hogar")

    # Presenta las opciones de compañías al usuario
    selected_company = cl.select("Por favor, seleccione la compañía:", options=companies)
    
    # Obtiene la pregunta del usuario
    query = cl.input("Haga una pregunta sobre la compañía:")
    
     # Genera y muestra la respuesta relevante
    answer = document_retriever.generate_answer(selected_company, query)
    cl.text(f"Respuesta: {answer}")
