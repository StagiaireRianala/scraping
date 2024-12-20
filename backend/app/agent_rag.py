from langchain.agents import Tool
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from app.pineconetest import search_pinecone
from dotenv import load_dotenv
import os

load_dotenv()

# Vérifiez que la clé est bien chargée
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Clé API OpenAI manquante. Assurez-vous que .env est configuré.")

# Initialisation OpenAI
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# Définir le modèle de prompt
custom_prompt = PromptTemplate(
    input_variables=["query", "context", "agent_scratchpad"],
    template=(
        "Tu es un expert en vente Amazon. Voici une question : {query}\n\n"
        "Contexte disponible : {context}\n\n"
        "Processus de raisonnement :\n{agent_scratchpad}\n\n"
        "Réponds de manière claire et détaillée en utilisant les informations fournies."
    )
)

# Définir les outils
pinecone_tool = Tool(
    name="Recherche Pinecone",
    func=search_pinecone,
    description="Cherche des informations pertinentes dans Pinecone pour une requête donnée."
)

from app.pineconetest import search_pinecone

def generate_response(query, context):
    """
    Combine la question et le contexte pour générer une réponse.
    """
    

    try:
        prompt = f"Voici une question : {query}\n\nContexte pertinent : {context}\n\n" \
                 "Réponds de manière claire et concise."
        response = llm.generate([prompt])
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Erreur lors de la génération de réponse : {e}")
        return "Erreur lors de la génération de la réponse."

def rag_agent(query):
    """
    Agent RAG qui exécute les étapes d'embedding, recherche, et génération de réponse.
    """
    try:
        # Recherche contextuelle avec Pinecone
        context = search_pinecone(query)

        # Génération de réponse avec LLM
        response = generate_response(query, context)
        return response
    except Exception as e:
        print(f"Erreur dans RAG Agent : {e}")
        return "Erreur lors de l'exécution de l'agent."
