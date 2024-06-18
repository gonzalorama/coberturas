import chainlit as cl
from src.langchain._document_retriever import CompanyDocumentRetriever
from chainlit.input_widget import Select

document_retriever = CompanyDocumentRetriever()
companies = ["Allianz", "Generali", "Liberty", "Mapfre", "Mutua Madrileña", "Occident", "Santa Lucía", "Zurich"]
companies=[
            cl.Action(name="allianz", value="allianz", label="Allianz"),
            cl.Action(name="generali", value="generali", label="Generali"),
            cl.Action(name="liberty", value="liberty", label="Liberty"),
            cl.Action(name="mapfre", value="mapfre", label="Mapfre"),
            cl.Action(name="mutua", value="mutua", label="Mutua Madrileña"),
            cl.Action(name="occident", value="occident", label="Occident"),
            cl.Action(name="santalucia", value="santalucia", label="Santa Lucía"),
            cl.Action(name="zurich", value="zurich", label="Zurich"),
        ]
@cl.on_chat_start
async def main():
    res = await cl.AskActionMessage(
        content="¡Hola, soy asesor de coberturas de seguros del Hogar!\n\nSelecciona tu compañia:",
        actions=companies,
    ).send()

    cl.user_session.set("company", res.get("value"))

    await cl.Message(
        content="¡Genial!, ¿Cúal es tu duda con tu póliza?",
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    company = cl.user_session.get("company")
    print(company)
    response = document_retriever.generate_answer(query=message.content, company_name=company)
    await cl.Message(response).send()