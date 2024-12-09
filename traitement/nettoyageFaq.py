import openai
import os
import json

# Configuration de l'API
openai.api_key =os.getenv("OPENAI_API_KEY")

# Fonction pour nettoyer le texte
def clean_text(text):
    import re
    text = text.strip().lower()
    text = re.sub(r"[^\w\s.,!?':-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

# Charger et nettoyer les données
file_path = "Public/faq_scraping_result.txt"
with open(file_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

# Diviser les sections par délimiteur
sections = raw_text.split("--------------------------------------------------")
cleaned_sections = [clean_text(section) for section in sections if section.strip()]

# Générer les embeddings
def generate_embeddings(sections):
    embeddings = []
    for section in sections:
        response = openai.Embedding.create(
            input=section,
            model="text-embedding-ada-002"  # Modèle recommandé pour les embeddings
        )
        embeddings.append(response['data'][0]['embedding'])
    return embeddings

embeddings = generate_embeddings(cleaned_sections)

# Exporter en JSON
output_file = "faq_embeddings.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(embeddings, json_file, ensure_ascii=False, indent=4)

print(f"Embeddings exportés avec succès dans '{output_file}'")
