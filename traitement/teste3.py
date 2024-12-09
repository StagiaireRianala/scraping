from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import random

# Configuration du WebDriver pour Chrome
options = webdriver.ChromeOptions()
#options.add_argument("--start-maximized")  # Ouvrir Chrome en plein écran
options.add_argument("--disable-blink-features=AutomationControlled")  # Désactiver détection d'automatisation
driver = webdriver.Chrome(options=options)

# URL cible
url = "https://sell.amazon.com/sell"
driver.get(url)

# Simulation de comportement humain
time.sleep(random.uniform(3, 6))  # Pause aléatoire

# Étape 1 : Extraire les titres (<h2>)
print("\n=== TITRES ===")
titles = driver.find_elements(By.CSS_SELECTOR, "h2.heading.align-start.font-size-xlarge.color-squid-ink.ember.font-heavy")
for title in titles:
    print("Titre:", title.text)

# Étape 2 : Extraire les titres (<h3>)
print("\n=== SOUS TITRES ===")
subtitles = driver.find_elements(By.CSS_SELECTOR, "h3.heading.align-start.font-size-large.color-squid-ink.ember.font-heavy")
for subtitle in subtitles:
    print("Sous Titre:", subtitle.text)

# Étape 3 : Extraire les contenus des <div> avec style=width:100%
print("\n=== CONTENUS ===")
divs = driver.find_elements(By.CSS_SELECTOR, "div[style='width:100%']")
for div in divs:
    # Contenu dans un <div class="text ...">
    text_divs = div.find_elements(By.CSS_SELECTOR, "div.text.align-start.color-storm.font-size-medium.ember.font-normal")
    for text_div in text_divs:
        print("Contenu (div.text):", text_div.text)

    # Contenu dans des listes <ul><li>
    list_items = div.find_elements(By.CSS_SELECTOR, "ul.list > li.color-storm.font-size-medium.ember")
    for item in list_items:
        print("Contenu (ul > li):", item.text)

     # Contenu dans des listes <ol><li>
    ol_items = div.find_elements(By.CSS_SELECTOR, "ol.list > li.color-storm.font-size-medium.ember ")
    for ol_item in ol_items:
        print("Contenu (ol > li):", ol_item.text)

# Contenus theme descri
print("\n=== contenus 123 ===")
contents = driver.find_elements(By.CSS_SELECTOR, "div[style='width:91.66666666666667%']")
for content in contents:
    try: 
        theme_element =content.find_element(By.CSS_SELECTOR, "div.text.align-start.color-squid-ink.font-size-default.ember.font-heavy")
        theme = theme_element.text.strip()
    except Exception as e:
        theme = "introuvable"    
    try:
        description_element = content.find_element(By.CSS_SELECTOR, "div.text.align-start.color-storm.font-size-small.ember.font-normal")
        description = description_element.text.strip()
    except Exception as e:
        description = "Réponse introuvable"

    print(f"theme: {theme}")     
    print(f"Réponse: {description}")
    print("-" * 50)


# Étape 4 : Extraire les liens (<a>)
print("\n=== LIENS ===")
links = driver.find_elements(By.CSS_SELECTOR, "a")
for link in links:
    href = link.get_attribute("href")
    if href:  # Ignorer les liens vides
        print("Lien:", href)

# Fermer le navigateur
driver.quit()
