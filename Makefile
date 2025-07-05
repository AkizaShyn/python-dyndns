include ../Makefile
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SERVICE_NAME=$(shell basename $(ROOT_DIR))

# --project_name must be in lowercase
SERVICE_NAME_LOWER=pythondyndns
# Git Folders
DOCKER_FOLDER=docker/
SECRET_FOLDER=secret/

# Remote Folders
INSTALL_FOLDER=/secret/$(SERVICE_NAME)/

DOCKER_FILE=-f $(DOCKER_FOLDER)docker-compose.yml 
DOCKER_COMMAND= $(ENV) docker compose -p $(SERVICE_NAME_LOWER) $(DOCKER_FILE)

install:
	@mkdir -p $(INSTALL_FOLDER)
	@cp -R $(SECRET_FOLDER)/* $(INSTALL_FOLDER)

start:
	$(DOCKER_COMMAND)  up -d --pull always
