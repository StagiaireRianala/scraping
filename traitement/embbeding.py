import json
import nltk
from nltk.tokenize import word_tokenize
import openai
import os

# Assurez-vous que le chemin vers le dossier nltk_data est correct
nltk.data.path.append('/Users/stagiaire_vyperf/nltk_data')

# Charger les données depuis un fichier JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Fonction pour diviser le texte en chunks de 200 à 500 mots
def split_into_chunks(text, min_chunk_size=200, max_chunk_size=500):
    words = word_tokenize(text)  # Tokeniser le texte en mots
    chunks = []
    start = 0
    
    # Diviser en chunks
    while start < len(words):
        end = min(start + max_chunk_size, len(words))
        chunk = words[start:end]
        
        # Si le chunk est trop petit, ajouter des mots pour respecter le min_chunk_size
        if len(chunk) < min_chunk_size and len(chunks) > 0:
            chunks[-1] += chunk  # Ajouter à l'ancien chunk
        else:
            chunks.append(chunk)
        
        start = end
    
    return chunks

# Fonction pour effectuer l'embedding avec OpenAI
def get_embedding(text, model="text-embedding-ada-002"):
    # Remplacez par votre clé API OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Appeler l'API d'OpenAI pour obtenir l'embedding
    response = openai.Embedding.create(model=model, input=text)
    return response['data'][0]['embedding']

# Fonction pour traiter un fichier JSON et obtenir des embeddings
def process_json_file(file_path, output_directory):
    data = load_json(file_path)

    # Traiter chaque item dans le fichier JSON
    for item in data:
        title = item['title']
        for subsection in item['subsections']:
            subtitle = subsection['subtitle']
            contents = subsection['contents']

            # Concaténer tous les contenus de la sous-section
            full_text = " ".join(contents)
            
            # Diviser le texte en chunks
            chunks = split_into_chunks(full_text)

            # Créer un nom de fichier basé sur le titre et le sous-titre
            file_name = f"{title}_{subtitle}_embeddings.json"
            file_name = file_name.replace("/", "_").replace("\\", "_")  # Remplacer les caractères invalides dans le nom de fichier

            # Créer un chemin pour le fichier de sortie
            output_file_path = os.path.join(output_directory, file_name)

            # Sauvegarder les embeddings dans un fichier JSON
            embeddings = []
            for idx, chunk in enumerate(chunks):
                chunk_text = " ".join(chunk)
                embedding = get_embedding(chunk_text)  # Obtenir l'embedding pour le chunk
                embeddings.append({
                    "chunk_id": idx + 1,
                    "embedding": embedding
                })

            # Enregistrer les embeddings dans un fichier JSON
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(embeddings, output_file, ensure_ascii=False, indent=4)

            print(f"Embeddings saved: {output_file_path}")

# Exemple d'utilisation
directory = 'output_doc/output_json'  # Répertoire contenant vos fichiers JSON
output_directory = 'output_embeddings'   # Répertoire de sortie pour les embeddings

# Créer le répertoire de sortie si nécessaire
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Traiter tous les fichiers JSON dans le répertoire et enregistrer les embeddings
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {filename}")
        process_json_file(file_path, output_directory)
