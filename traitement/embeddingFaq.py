import openai

# Configuration de l'API
openai.api_key = "YOUR_OPENAI_API_KEY"

# Générer les embeddings
def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = openai.Embedding.create(
            input=chunk,
            model="text-embedding-ada-002"  # Modèle recommandé pour les embeddings
        )
        embeddings.append(response['data'][0]['embedding'])
    return embeddings

embeddings = generate_embeddings(chunks)
print(f"Nombre d'embeddings générés : {len(embeddings)}")
