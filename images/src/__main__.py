"""
Script de synchronisation DNS IONOS :
- Récupère l'IP publique du serveur
- Récupère l'IP actuelle du domaine configuré sur IONOS
- Compare les deux et logue l'état

Nécessite les variables d'environnement :
- API_KEY
- ZONE_ID
- SUFFIX
"""
import logging
import os
import sys
from datetime import datetime
import requests


LOG_FILE = f"logs/{datetime.now().strftime('%Y-%m-%d')}_dyndns.log"
logging.basicConfig(
    filename=LOG_FILE,  # Nom du fichier de log
    level=logging.INFO,              # Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format des messages
    datefmt='%Y-%m-%d %H:%M:%S'      # Format de la date/heure
)

# Ajoute un handler console en plus du fichier
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)


def get_env_var(name: str) -> str:
    """Function pour récupérer les variables dans le .env"""
    value = os.environ.get(name)
    if not value:
        logging.critical("La variable d'environnement %s est manquante.", name)
        sys.exit(1)
    return value


def main():
    """"Fonction principale"""

    # configuration des variables
    api_key = get_env_var("API_KEY")
    zone_id = get_env_var("ZONE_ID")
    suffix = get_env_var("SUFFIX")


    url = f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}"
    headers = {
        "X-API-Key": api_key
    }
    params = {
        "suffix": suffix,
        "recordType": "A"
    }

    # récupérer ip sur ionos
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        ionosip = response.json()["records"][0]["content"]

    except requests.RequestException as e:
        logging.critical("Erreur API IONOS : %s", e)
        sys.exit(1)

    except (KeyError, IndexError) as e:
        logging.critical("Erreur de parsing JSON IONOS : %s", e)
        sys.exit(1)

    logging.info("Adresse IP enregistrée chez IONOS : %s", ionosip)


    # récupérer valeur de mon ip
    try:
        my_public_ip = requests.get("https://api.ipify.org", timeout=5).text
        logging.info('Mon adresse publique est : %s', my_public_ip)
    except requests.RequestException as e:
        logging.critical("Erreur lors de la récupération de l'IP publique : %s", e)
        sys.exit(1)

    # Comparaison
    if ionosip != my_public_ip:
        logging.info("L'ip publique est différente de l'ip sur le nom de domaine ionos")
    else:
        logging.info("les ip sont identiques")

    # notifier sur discord du changement avec ip précédente et nouvelle ip


if __name__ == "__main__":
    main()
