from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Configuration du WebDriver pour Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # Désactiver détection d'automatisation
driver = webdriver.Chrome(options=options)

# URL cible
url = "https://sell.amazon.com/sell"
driver.get(url)

# Simulation de comportement humain
time.sleep(random.uniform(3, 6))  # Pause aléatoire

# Étape 5 : produit <div>class="accordion accordion-border-top accordion-type-light expanded"
print("\n=== FAQ ===")
faq_contexte = []

try:
    # Attendre la présence des éléments FAQ
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[itemtype='https://schema.org/Question']")))
    faq_elements = driver.find_elements(By.CSS_SELECTOR, "div[itemtype='https://schema.org/Question']")

    # Parcourir les éléments FAQ
    for faq in faq_elements:
        question_element = faq.find_element(By.CSS_SELECTOR, "div.title.align-start")
        question = question_element.text.strip()

        try:
            # Cliquer pour afficher la réponse
            question_element.click()
            time.sleep(1)  
        except Exception as e:
            print(f"Impossible de cliquer sur la FAQ : {e}")

        try:
            # Récupérer la réponse
            answer_element = faq.find_element(By.CSS_SELECTOR, "div[itemprop='text']")
            answer = answer_element.text.strip()
        except Exception as e:
            answer = "Réponse introuvable"

        # Ajouter la question et réponse au contexte
        faq_contexte.append(f"Question: {question}\nRéponse: {answer}\n" + "-" * 50)

        # Afficher dans la console
        print(f"Question: {question}")
        print(f"Réponse: {answer}")
        print("-" * 50)

except Exception as e:
    print("Erreur pendant le scraping :", e)

# Enregistrement dans un fichier texte
output_file = "faq_scraping_result.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(faq_contexte))

print(f"Les résultats ont été sauvegardés dans le fichier : {output_file}")

# Fermer le navigateur
driver.quit()
