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

# Étape 2 : Extraire tous les liens (<a>) au sein des sections analysées
all_links = driver.find_elements(By.CSS_SELECTOR, "a")
for link in all_links:
    href = link.get_attribute("href")
    if href:
        if current_subtitle:
            current_subtitle["links"].append(href)
        elif current_title:
            current_title["links"].append(href)

# Afficher les résultats structurés
print("\n=== RÉSULTATS STRUCTURÉS ===")
for section in data:
    print(f"\nTitre : {section['title']}")
    print("Thèmes et descriptions associés :")
    for theme_and_desc in section["themes_and_descriptions"]:
        print(f"  - Thème : {theme_and_desc['theme']}, Description : {theme_and_desc['description']}")
    for subtitle in section["subtitles"]:
        print(f"  Sous-titre : {subtitle['subtitle']}")
        print("  Contenus :")
        for content in subtitle["contents"]:
            print(f"    - {content}")
        print("  Thèmes associés :")
        for theme_and_desc in subtitle["themes_and_descriptions"]:
            print(f"    - Thème : {theme_and_desc['theme']}, Description : {theme_and_desc['description']}")
    print("Contenus hors sous-titres :")
    for content in section["contents"]:
        print(f"  - {content}")
    print("Liens associés :")
    for link in section["links"]:
        print(f"  - {link}")

# Fermer le navigateur
driver.quit()
