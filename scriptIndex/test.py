import os
import openai
from pinecone import Pinecone, ServerlessSpec

# Clés API
PINECONE_API_KEY ="pcsk_57fznT_QX1C6GeWTZGNbDL99sGggmJessNvX4FzY4xY8BadavjBckCvfanNiH2enpuZkg4"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_ENVIRONMENT = "us-east-1"  # Région de Pinecone
INDEX_NAME = "agentrag"

# Initialisation des APIs
openai.api_key = OPENAI_API_KEY
pc = Pinecone(api_key=PINECONE_API_KEY)

# Connexion à l'index
index = pc.Index(INDEX_NAME)

# Recherche dans l'index
def search_in_index(query_text, namespace="default_namespace"):
    print("\n[TEST] Recherche dans l'index...")

    # Générer l'embedding pour la requête
    embedding_response = openai.Embedding.create(
        input=query_text,
        model="text-embedding-ada-002"
    )
    query_vector = embedding_response["data"][0]["embedding"]

    # Rechercher les vecteurs les plus proches
    results = index.query(
        vector=query_vector,
        top_k=5,  # Nombre de résultats à retourner
        include_metadata=True,  # Inclure les métadonnées dans les résultats
        namespace=namespace  # Spécifiez le namespace si nécessaire
    )

    # Afficher les résultats
    print(f"Résultats pour la requête : '{query_text}'")
    for match in results["matches"]:
        print(f"ID : {match['id']}, Score : {match['score']},emb : {match['values']}, Métadonnées : {match['metadata']}")

# Exemple de requête
if __name__ == "__main__":
    query = "comment vendre sur amazon ?"
    search_in_index(query_text=query, namespace="agentrag_namespace")
result = index.fetch(ids=["chunk-19"], namespace="agentrag_namespace")

