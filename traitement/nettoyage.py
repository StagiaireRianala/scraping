import os
import json

def nettoyer_donnees_fichier(input_file):
    """
    Nettoie un fichier texte brut, retire les champs vides et retourne une structure de données JSON.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        raw_data = file.read()

    structured_data = []
    current_title = None
    current_subtitle = None
    current_content = []
    current_themes = []

    for line in raw_data.splitlines():
        line = line.strip()
        
        # Détecter un titre principal
        if line.startswith("Titre :"):
            if current_title:
                # Sauvegarder le bloc précédent
                if subsections:  # Ajouter uniquement si des sous-sections existent
                    structured_data.append({
                        "title": current_title,
                        "subsections": subsections,
                    })
            current_title = line.replace("Titre :", "").strip()
            subsections = []  # Réinitialiser les sous-sections

        # Détecter un sous-titre
        elif line.startswith("Sous-titre :"):
            if current_subtitle:
                # Ajouter le sous-titre précédent aux sous-sections
                if current_content or current_themes:  # Ajouter uniquement si contenu ou thèmes
                    subsections.append({
                        "subtitle": current_subtitle,
                        "contents": current_content,
                        "themes": current_themes,
                    })
            current_subtitle = line.replace("Sous-titre :", "").strip()
            current_content = []
            current_themes = []

        # Détecter les contenus
        elif line.startswith("Contenus :"):
            current_content = []

        # Ajouter des points de contenu
        elif line.startswith("-") or line.startswith("•"):
            current_content.append(line.lstrip("-• ").strip())

        # Ajouter des thèmes associés
        elif line.startswith("Thèmes associés :"):
            current_themes = []

        # Ajouter des lignes de thèmes associés
        elif current_themes is not None:
            if line:
                current_themes.append(line)

    # Ajouter le dernier titre et sous-titre
    if current_title:
        if current_content or current_themes:  # Vérifier qu'il y a des contenus à sauvegarder
            subsections.append({
                "subtitle": current_subtitle,
                "contents": current_content,
                "themes": current_themes,
            })
        if subsections:  # Ajouter uniquement si des sous-sections existent
            structured_data.append({
                "title": current_title,
                "subsections": subsections,
            })

    return structured_data


def traiter_dossier(input_folder, output_folder):
    """
    Parcourt tous les fichiers .txt dans un dossier, nettoie leur contenu et génère des fichiers JSON.
    """
    # Vérifier que le dossier de sortie existe, sinon le créer
    os.makedirs(output_folder, exist_ok=True)

    # Parcourir tous les fichiers du dossier d'entrée
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Traiter uniquement les fichiers texte
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".txt", ".json"))

            # Nettoyer le fichier
            print(f"Traitement de {filename}...")
            cleaned_data = nettoyer_donnees_fichier(input_path)

            # Exporter en JSON
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)

            print(f"Fichier nettoyé exporté : {output_path}")


# Appeler la fonction avec le dossier parent
input_folder = "output_text_files"  # Remplacez par le chemin de votre dossier contenant les fichiers
output_folder = "output_json"  # Dossier pour enregistrer les fichiers JSON
traiter_dossier(input_folder, output_folder)
