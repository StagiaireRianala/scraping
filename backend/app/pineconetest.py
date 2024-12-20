import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import OpenAIEmbeddings

# Clé API et configuration
PINECONE_API_KEY = "pcsk_57fznT_QX1C6GeWTZGNbDL99sGggmJessNvX4FzY4xY8BadavjBckCvfanNiH2enpuZkg4"
PINECONE_ENVIRONMENT = "us-east-1"
INDEX_NAME = "agentrag"

# Créer une instance de Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Vérifier si l'index existe déjà, sinon le créer
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # Changez cette valeur selon la taille de vos embeddings
        metric="cosine",  # Utilisez une métrique adaptée
        spec=ServerlessSpec(
            cloud="aws",
            region=PINECONE_ENVIRONMENT  # Région du cluster
        )
    )

# Récupérer l'index
index = pc.Index(INDEX_NAME)

print(f"Index '{INDEX_NAME}' initialisé avec succès.")

# Exemple de recherche
from langchain_openai import OpenAIEmbeddings

OPENAI_API_KEY = "sk-proj-mFgBvH0lQ9xrwqfDf0MxT3BlbkFJFNTQehkUIYIJG9yE5GQn"
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def search_pinecone(query):
    """
    Génère l'embedding de la question et recherche le contexte dans Pinecone.
    """
    try:
        query_vector = embeddings.embed_query(query)  # Générer l'embedding
        result = index.similarity_search_by_vector(query_vector, top_k=3)  # Rechercher
        context = "\n".join([doc.page_content for doc in result])
        return context
    except Exception as e:
        print(f"Erreur lors de la recherche Pinecone : {e}")
        return None
from langchain.llms import OpenAI

