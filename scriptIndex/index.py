import os
import openai
from pinecone import Pinecone, ServerlessSpec

# Clés API
PINECONE_API_KEY = "pcsk_57fznT_QX1C6GeWTZGNbDL99sGggmJessNvX4FzY4xY8BadavjBckCvfanNiH2enpuZkg4"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_ENVIRONMENT = "us-east-1"  # Remplacez par votre région si nécessaire
INDEX_NAME = "agentrag"

# Initialisation de l'API OpenAI
openai.api_key = OPENAI_API_KEY

# Initialisation de Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Vérification et création de l'index si nécessaire
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # Dimension des vecteurs générés par OpenAI
        metric="cosine",  # Mesure de similarité
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
    )

# Connexion à l'index
index = pc.Index(INDEX_NAME)

# Fonction pour lire et chunker un fichier
def chunk_file(file_path, file_name):
    import re
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Regex pour capturer les titres et contenus associés
    pattern = r"Titre : (.+?)\nContenus?(?: hors Titres)? :\n([\s\S]*?)(?=\nTitre|$)"
    matches = re.findall(pattern, content, re.DOTALL)

    chunks = []
    for i, (title, text) in enumerate(matches):
        text = text.strip().replace("\n", " ").strip()
        # Inclure le nom du fichier dans l'ID
        chunk_id = f"{file_name}-chunk-{i+1}"
        chunks.append({
            "id": chunk_id,
            "texte": text,
            "theme": title.strip()
        })
    return chunks

# Fonction pour générer des embeddings et les stocker dans Pinecone
def process_and_store_chunks(directory_path):
    all_chunks = []
    global_chunk_id = 1  # Initialiser un compteur global

    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory_path, file_name)
            chunks = chunk_file(file_path, file_name)

            for chunk in chunks:
                # Ajouter un ID global unique
                chunk["id"] = f"chunk-{global_chunk_id}"
                global_chunk_id += 1

                # Générer embedding
                response = openai.Embedding.create(
                    input=chunk["texte"],
                    model="text-embedding-ada-002"
                )
                chunk["embedding"] = response["data"][0]["embedding"]

                # Prévisualiser avant stockage
                print(f"ID : {chunk['id']}")
                print(f"Texte : {chunk['texte']}")
                print(f"Thème : {chunk['theme']}")
                print("-" * 50)

                # Stocker dans Pinecone
                index.upsert(
                    vectors=[
                        {
                            "id": chunk["id"],
                            "values": chunk["embedding"],
                            "metadata": {
                                "texte": chunk["texte"],
                                "theme": chunk["theme"]
                            }
                        }
                    ],
                    namespace="agentrag_namespace"  # Namespace pour organiser les vecteurs
                )

            all_chunks.extend(chunks)

    return all_chunks

# Chemin du dossier contenant les fichiers
directory_path = "/Users/stagiaire_vyperf/Documents/Rianala/scraping/scriptIndex/output_text_files"  # Remplacez par le chemin réel
all_chunks = process_and_store_chunks(directory_path)

print("Tous les fichiers ont été traités et stockés dans Pinecone.")
