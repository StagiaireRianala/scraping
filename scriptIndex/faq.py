import os
import openai
from pinecone import Pinecone, ServerlessSpec

# Clés API
PINECONE_API_KEY = "pcsk_57fznT_QX1C6GeWTZGNbDL99sGggmJessNvX4FzY4xY8BadavjBckCvfanNiH2enpuZkg4"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_ENVIRONMENT = "us-east-1"  # Région de Pinecone
INDEX_NAME = "faqindex"

# Initialisation des APIs
openai.api_key = OPENAI_API_KEY
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

# Fonction pour lire et chunker une FAQ
def process_faq_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Diviser les FAQ en blocs par les lignes de séparation
    faqs = content.split("--------------------------------------------------")
    chunks = []

    for i, faq in enumerate(faqs):
        if not faq.strip():  # Ignorer les blocs vides
            continue
        
        # Extraire la question et la réponse
        lines = faq.strip().split("\n")
        question_line = next((line for line in lines if line.startswith("Question:")), None)
        answer_line = next((line for line in lines if line.startswith("Réponse:")), None)

        if question_line and answer_line:
            question = question_line.replace("Question: ", "").strip()
            answer = answer_line.replace("Réponse: ", "").strip()

            # Créer un chunk avec ID unique
            chunk_id = f"faq-{i+1}"
            chunks.append({
                "id": chunk_id,
                "question": question,
                "answer": answer,
                "texte": f"Question: {question}\nRéponse: {answer}"
            })
    return chunks

# Fonction pour générer des embeddings et les stocker dans Pinecone
def process_and_store_faqs(directory_path):
    all_faqs = []
    global_chunk_id = 1  # Initialiser un compteur global

    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory_path, file_name)
            faqs = process_faq_file(file_path)

            for faq in faqs:
                # Ajouter un ID global unique
                faq["id"] = f"faq-{global_chunk_id}"
                global_chunk_id += 1

                # Générer embedding
                response = openai.Embedding.create(
                    input=faq["texte"],
                    model="text-embedding-ada-002"
                )
                faq["embedding"] = response["data"][0]["embedding"]

                # Prévisualiser avant stockage
                print(f"ID : {faq['id']}")
                print(f"Question : {faq['question']}")
                print(f"Réponse : {faq['answer']}")
                print("-" * 50)

                # Stocker dans Pinecone
                index.upsert(
                    vectors=[
                        {
                            "id": faq["id"],
                            "values": faq["embedding"],
                            "metadata": {
                                "question": faq["question"],
                                "answer": faq["answer"]
                            }
                        }
                    ],
                    namespace="faq_namespace"  # Namespace pour organiser les vecteurs
                )

            all_faqs.extend(faqs)

    return all_faqs

# Chemin du dossier contenant les fichiers FAQ
directory_path = "/Users/stagiaire_vyperf/Documents/Rianala/scraping/scriptIndex/faq"  # Remplacez par le chemin réel
all_faqs = process_and_store_faqs(directory_path)

print("Toutes les FAQ ont été traitées et stockées dans Pinecone.")
