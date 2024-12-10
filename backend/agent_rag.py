# -*- coding: utf-8 -*-

from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent, Tool
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone
from dotenv import os 
import pinecone

# Clés API
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = "agentrag"

# Initialisation de Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment="us-east-1")
index = Pinecone.from_existing_index(index_name=INDEX_NAME, embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))

# Définir l'outil Pinecone
def search_pinecone_tool(query):

    """Recherche dans Pinecone les documents pertinents pour la requête."""
    result = index.similarity_search(query, top_k=3)  # Top 3 documents pertinents
    return "\n".join([doc.page_content for doc in result])

pinecone_tool = Tool(
    name="Recherche Pinecone",
    func=search_pinecone_tool,
    description="Cherche des informations pertinentes dans Pinecone pour une requête donnée."
)

# Prompt personnalisé
custom_prompt = PromptTemplate(
    input_variables=["query", "context"],
    template=(
        "Tu es un expert en vente Amazon. Voici une question : {query}\n\n"
        "Contexte disponible : {context}\n\n"
        "Réponds de manière claire et détaillée en utilisant les informations fournies."
    )
)

# Initialisation du LLM OpenAI
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# Liste des outils
tools = [pinecone_tool]

# Création de l'agent via create_openai_tools_agent
agent = create_openai_tools_agent(
    llm=llm,
    tools=tools,
    prompt=custom_prompt  # Utilisation du prompt personnalisé ici
)

# Exécution de l'agent
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Poser une question à l'agent
question = "Quels sont les frais pour devenir vendeur sur Amazon ?"

# Recherche du contexte via Pinecone
context = search_pinecone_tool(question)

# Exécution finale en utilisant le prompt personnalisé
response = llm.generate(custom_prompt.format(query=question, context=context))

print("Réponse de l'agent :", response)
