.PHONY: help install run docker-build docker-run docker-stop clean test

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make run          - Run application locally"
	@echo "  make process      - Process documents"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run with Docker Compose"
	@echo "  make docker-stop  - Stop Docker containers"
	@echo "  make clean        - Clean cache and temp files"
	@echo "  make deploy-k8s   - Deploy to Kubernetes"

install:
	pip install -r requirements.txt

run:
	streamlit run src/main.py

process:
	python src/process_docs.py

docker-build:
	docker build -t fcj-chatbot .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete

deploy-k8s:
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/pvc.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
