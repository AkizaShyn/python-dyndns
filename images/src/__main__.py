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
    log_level_str = get_env_var("LOG_LEVEL")
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)


    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}_dyndns.log"
    logging.basicConfig(
    filename=log_file,  # Nom du fichier de log
    level=log_level,              # Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format des messages
    datefmt='%Y-%m-%d %H:%M:%S'      # Format de la date/heure
    )

    # Ajoute un handler console en plus du fichier
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)



    url = f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}"
    headers = {
        "X-API-Key": api_key,
        "accept": "application/json"
    }
    params = {
        "suffix": suffix,
        "recordType": "A"
    }

    # récupérer ip sur ionos
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        logging.debug("Contenu de response %s", response.json())
        response.raise_for_status()
        ionos_ip = response.json()["records"][0]["content"]
        ionos_ip_id = response.json()["records"][0]["id"]
        logging.debug("Contenu de ionosipid %s", ionos_ip_id)

    except requests.RequestException as e:
        logging.critical("Erreur API IONOS : %s", e)
        sys.exit(1)

    except (KeyError, IndexError) as e:
        logging.critical("Erreur de parsing JSON IONOS : %s", e)
        sys.exit(1)

    logging.info("Adresse IP enregistrée chez IONOS : %s", ionos_ip)


    # récupérer valeur de mon ip
    try:
        my_public_ip = requests.get("https://api.ipify.org", timeout=5).text
        logging.info('Mon adresse publique est : %s', my_public_ip)
    except requests.RequestException as e:
        logging.critical("Erreur lors de la récupération de l'IP publique : %s", e)
        sys.exit(1)

    # Comparaison
    if ionos_ip != my_public_ip:
        logging.info("L'ip publique est différente de l'ip sur le nom de domaine ionos")
        logging.info("Lancement changement de l'ip du nom de domaine")
        try:
            url = f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}/records/{ionos_ip_id}"
            headers = {
                "X-API-Key": api_key
            }
            payload = {
                "data": {
                    "type": "record",
                    "id": ionos_ip_id,
                    "attributes": {
                        "content": my_public_ip
                    }
                }
            }
            response = requests.put(url, headers=headers, json=payload, timeout=5)
            response.raise_for_status()
            logging.debug("Contenu de response %s", response.json())

        except requests.RequestException as e:
            logging.critical("Erreur API IONOS : %s", e)
            sys.exit(1)

        except (KeyError, IndexError) as e:
            logging.critical("Erreur de parsing JSON IONOS : %s", e)
            sys.exit(1)


    else:
        logging.info("les ip sont identiques")


if __name__ == "__main__":
    main()
