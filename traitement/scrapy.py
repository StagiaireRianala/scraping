import os
from selenium.webdriver.common.by import By
from selenium import webdriver
import logging
import time
import random

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration du WebDriver pour Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

url = "https://sell.amazon.com/sell"
driver.get(url)

# Simulation de comportement humain
time.sleep(random.uniform(3, 6))  # Pause aléatoire pour éviter la détection automatique

# Initialisation des structures de données
data = []  # Liste pour stocker les données structurées
current_title = None
current_subtitle = None

# Étape 1 : Parcourir tous les éléments et détecter les titres, sous-titres, contenus, thèmes, descriptions, et contenus spécifiques
elements = driver.find_elements(By.XPATH, "//h2 | //h3 | //div[contains(@class,'text')] | //ul[contains(@class, 'list')] | //ol[contains(@class, 'list')]")

for element in elements:
    try:
        element_class = element.get_attribute("class") or ""
        element_tag = element.tag_name or ""

        # Vérifier si c'est un titre (<h2>)
        if element_tag == "h2" and "font-size-xlarge" in element_class:
            if current_title:
                data.append(current_title)
            current_title = {
                "title": element.text.strip(),
                "subtitles": [],
                "contents": [],
                "themes_and_descriptions": [],
                "links": [],
            }
            current_subtitle = None
            logging.info(f"Titre trouvé : {current_title['title']}")

        # Vérifier si c'est un sous-titre (<h3>)
        elif element_tag == "h3" and "font-size-large" in element_class:
            if current_title:
                current_subtitle = {
                    "subtitle": element.text.strip(),
                    "contents": [],
                    "themes_and_descriptions": [],
                    "links": [],
                }
                current_title["subtitles"].append(current_subtitle)
                logging.info(f"Sous-titre trouvé : {current_subtitle['subtitle']}")

        # Traitement des contenus div (contenus généraux)
        elif element_tag == "div" and "text" in element_class:
            content = element.text.strip()

            if current_subtitle:
                current_subtitle["contents"].append(content)
            elif current_title:
                current_title["contents"].append(content)

        # Traitement des contenus spécifiques (themes et descriptions)
        elif element_tag == "div" and element.get_attribute("style") == "width:91.66666666666667%":
            try:
                theme_element = element.find_element(By.CSS_SELECTOR, "div.text.align-start.color-squid-ink.font-size-default.ember.font-heavy")
                theme = theme_element.text.strip()
            except Exception:
                theme = "introuvable"

            try:
                description_element = element.find_element(By.CSS_SELECTOR, "div.text.align-start.color-storm.font-size-small.ember.font-normal")
                description = description_element.text.strip()
            except Exception:
                description = "Réponse introuvable"

            theme_and_description = {"theme": theme, "description": description}
            if current_subtitle:
                current_subtitle["themes_and_descriptions"].append(theme_and_description)
            elif current_title:
                current_title["themes_and_descriptions"].append(theme_and_description)

            logging.info(f"Thème : {theme}, Description : {description}")

        # Traitement des listes (ul > li et ol > li)
        elif element_tag in ["ul", "ol"]:
            list_items = element.find_elements(By.TAG_NAME, "li")
            for li in list_items:
                content = li.text.strip()
                if current_subtitle:
                    current_subtitle["contents"].append(content)
                elif current_title:
                    current_title["contents"].append(content)

    except Exception as e:
        logging.error(f"Erreur lors de l'extraction de l'élément : {e}")

# Ajouter la dernière section
if current_title:
    data.append(current_title)

# Étape 2 : Écrire chaque titre et ses données associées dans un fichier .txt distinct
output_folder = "output_text_files"
os.makedirs(output_folder, exist_ok=True)  # Créer un dossier pour stocker les fichiers .txt

for section in data:
    filename = f"{section['title'].replace('/', '-').replace(':', '-')}.txt"  # Nom du fichier basé sur le titre
    file_path = os.path.join(output_folder, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        # Écrire le titre principal
        file.write(f"Titre : {section['title']}\n")
        file.write("=" * 50 + "\n")

        # Écrire les thèmes et descriptions associés
        if section["themes_and_descriptions"]:
            file.write("\nThèmes et descriptions associés :\n")
            for theme_and_desc in section["themes_and_descriptions"]:
                file.write(f"  - Thème : {theme_and_desc['theme']}, Description : {theme_and_desc['description']}\n")

        # Écrire les sous-titres et leurs contenus
        for subtitle in section["subtitles"]:
            file.write(f"\nSous-titre : {subtitle['subtitle']}\n")
            file.write("-" * 50 + "\n")
            file.write("Contenus :\n")
            for content in subtitle["contents"]:
                file.write(f"    - {content}\n")
            file.write("Thèmes associés :\n")
            for theme_and_desc in subtitle["themes_and_descriptions"]:
                file.write(f"    - Thème : {theme_and_desc['theme']}, Description : {theme_and_desc['description']}\n")

        # Écrire les contenus hors sous-titres
        if section["contents"]:
            file.write("\nContenus hors sous-titres :\n")
            for content in section["contents"]:
                file.write(f"  - {content}\n")

        # Écrire les liens associés
        if section["links"]:
            file.write("\nLiens associés :\n")
            for link in section["links"]:
                file.write(f"  - {link}\n")

    logging.info(f"Fichier créé : {file_path}")

# Fermer le navigateur
driver.quit()
