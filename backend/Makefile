# Makefile for Hybrid Chatbot System

.PHONY: help install run test clean docker-build docker-up docker-down populate health lint format

# Variables
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker-compose
VENV := venv
APP_NAME := chatbot-hybrid

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo "$(GREEN)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)Installing dependencies...$(NC)"
	./$(VENV)/bin/$(PIP) install -r requirements.txt
	@echo "$(GREEN)Installation complete!$(NC)"

run: ## Run the application (Flask by default)
	@echo "$(GREEN)Starting Flask server...$(NC)"
	$(PYTHON) main.py

run-fastapi: ## Run with FastAPI
	@echo "$(GREEN)Starting FastAPI server...$(NC)"
	USE_FASTAPI=true $(PYTHON) main.py

run-dev: ## Run in development mode with auto-reload
	@echo "$(GREEN)Starting in development mode...$(NC)"
	DEBUG=true $(PYTHON) main.py

test: ## Run all tests
	@echo "$(GREEN)Running tests...$(NC)"
	pytest tests/ -v

test-unit: ## Run unit tests only
	@echo "$(GREEN)Running unit tests...$(NC)"
	pytest tests/unit/ -v

test-integration: ## Run integration tests only
	@echo "$(GREEN)Running integration tests...$(NC)"
	pytest tests/integration/ -v

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	pytest tests/ --cov=app --cov-report=html --cov-report=term
	@echo "$(GREEN)Coverage report generated in htmlcov/index.html$(NC)"

clean: ## Clean up cache and temporary files
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	@echo "$(GREEN)Clean complete!$(NC)"

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	$(DOCKER_COMPOSE) build

docker-up: ## Start Docker containers
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Containers started! Check logs with: docker-compose logs -f$(NC)"

docker-down: ## Stop Docker containers
	@echo "$(YELLOW)Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) down

docker-logs: ## Show Docker logs
	$(DOCKER_COMPOSE) logs -f

docker-shell: ## Open shell in app container
	$(DOCKER_COMPOSE) exec chatbot /bin/bash

populate: ## Populate the vector database
	@echo "$(GREEN)Populating database...$(NC)"
	$(PYTHON) scripts/populate_db.py populate

verify-db: ## Verify database contents
	@echo "$(GREEN)Verifying database...$(NC)"
	$(PYTHON) scripts/populate_db.py verify

clear-db: ## Clear the database
	@echo "$(RED)Clearing database...$(NC)"
	$(PYTHON) scripts/populate_db.py clear

health: ## Run health check
	@echo "$(GREEN)Running health check...$(NC)"
	$(PYTHON) scripts/health_check.py

health-watch: ## Run continuous health monitoring
	@echo "$(GREEN)Starting health monitoring...$(NC)"
	$(PYTHON) scripts/health_check.py --continuous

lint: ## Run code linting
	@echo "$(GREEN)Running linters...$(NC)"
	flake8 app/ tests/
	mypy app/

format: ## Format code with black
	@echo "$(GREEN)Formatting code...$(NC)"
	black app/ tests/ scripts/
	isort app/ tests/ scripts/

requirements: ## Update requirements.txt
	@echo "$(GREEN)Updating requirements...$(NC)"
	./$(VENV)/bin/pip freeze > requirements.txt

env-example: ## Create .env from .env.example
	@echo "$(GREEN)Creating .env file...$(NC)"
	cp .env.example .env
	@echo "$(YELLOW)Please edit .env with your configuration$(NC)"

monitoring: ## Open monitoring dashboard
	@echo "$(GREEN)Opening monitoring dashboard...$(NC)"
	@python -m webbrowser http://localhost:5000/api/monitoring/dashboard

docs: ## Generate documentation
	@echo "$(GREEN)Generating documentation...$(NC)"
	sphinx-build -b html docs/ docs/_build/html
	@echo "$(GREEN)Documentation generated in docs/_build/html/$(NC)"

backup: ## Backup database and configurations
	@echo "$(GREEN)Creating backup...$(NC)"
	mkdir -p backups
	tar -czf backups/backup-$$(date +%Y%m%d-%H%M%S).tar.gz \
		app/data/database \
		app/data/documents \
		.env
	@echo "$(GREEN)Backup created in backups/$(NC)"

restore: ## Restore from latest backup
	@echo "$(YELLOW)Restoring from latest backup...$(NC)"
	@if [ -z "$$(ls -A backups 2>/dev/null)" ]; then \
		echo "$(RED)No backups found!$(NC)"; \
	else \
		tar -xzf $$(ls -t backups/*.tar.gz | head -1); \
		echo "$(GREEN)Restored from $$(ls -t backups/*.tar.gz | head -1)$(NC)"; \
	fi

all: clean install populate test ## Clean, install, populate DB and test

dev-setup: install env-example populate ## Complete development setup

prod-deploy: docker-build docker-up populate ## Deploy to production with Docker

.DEFAULT_GOAL := help
