import requests
from bs4 import BeautifulSoup

def telecharger_et_sauvegarder_html(url, fichier_sortie):
    try:
        # Envoyer la requête HTTP
        reponse = requests.get(url)
        reponse.raise_for_status()  # Lève une erreur si le statut n'est pas 200

        # Utiliser BeautifulSoup pour parser le HTML
        soup = BeautifulSoup(reponse.text, 'html.parser')

        # Obtenir le HTML formaté
        html_formatte = soup.prettify()

        # Écrire dans un fichier HTML
        with open(fichier_sortie, 'w', encoding='utf-8') as fichier:
            fichier.write(html_formatte)

        print(f"Le code source a été sauvegardé dans '{fichier_sortie}'")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page : {e}")

# Exemple d'utilisation
url = "https://purplerouen.fr/"
fichier_sortie = "page_exemple.html"
telecharger_et_sauvegarder_html(url, fichier_sortie)
