# python-dyndns

## Introduction

Le but de ce repos est de mettre à jour un nom de domaine en fonction de son ip publique de façon automatique

## Installation

### Prérequis

docker docker compose make installés

Faire `make install`, éditez ensuite le fichier `./docker/.env`
Compléter les variables

API_KEY - Correspond à la clé d'api chez ionos
ZONE_ID - correspon à l'id de la zone du domaine
SUFFIX - correspond au domaine a éditer (toto.toto.fr par exemple)
LOG_LEVEL - par défaut INFO peut-être édité pour avoir plus de logs

## Utilisation

`make build` pour build l'image
`make start` pour lancer le script

## logs

les logs sont disponibles dans ./logs
