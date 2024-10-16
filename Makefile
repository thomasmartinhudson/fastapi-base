# Directories
BACKEND_DIR := ./backend
FRONTEND_DIR := ./frontend

# Local Docker Compose
FASTAPI_PROJECT_NAME := fastapi-base
FASTAPI_LOCAL_COMPOSE_FILE := docker-compose-local.yml
FASTAPI_BACKEND_SERVICE := fastapi-backend
DEV_ENV_FILE_PATH := ./backend/dev.env
COMPOSE_LOCAL_FASTAPI := docker compose -f $(FASTAPI_LOCAL_COMPOSE_FILE) -p $(FASTAPI_PROJECT_NAME) --env-file ${DEV_ENV_FILE_PATH}

.PHONY: help
help:					## Show the help.
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

backend-install:			## Install the project in dev mode.
	@make --directory=$(BACKEND_DIR) -s backend-install

backend-show:				## Show the backend environment.
	@make --directory=$(BACKEND_DIR) -s backend-show

backend-lint:				## Apply all Python linting operations (as per CI)
	@make --directory=$(BACKEND_DIR) -s backend-lint

fastapi-run-local-debug:		## Compose all local debug containers to run in debug mode
	make -s fastapi-kill
	@$(NINE_DEV) -- ${COMPOSE_LOCAL_FASTAPI} up --build

fastapi-kill:				## Kill all local debug containers
	@docker compose -p $(FASTAPI_PROJECT_NAME) down
