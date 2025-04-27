ENV_FILE := .env
K8S_DIR := k8s
DOCKER_REGISTRY := docker.io/amsg08
KAFKA_UI_PORT := 8081
KIBANA_PORT := 5601
PROM_PORT := 9090
GRAFANA_PORT := 3000

.DEFAULT_GOAL := help

$(ENV_FILE):
	@echo "[Generating .env file...]"
	@echo "MINIKUBE_IP=$$(minikube ip)" > $(ENV_FILE)
	@echo "KAFKA_BROKER=kafka:9092" >> $(ENV_FILE)
	@echo "KAFKA_TOPIC=wiki-events" >> $(ENV_FILE)
	@echo "PRODUCER_PORT=8000" >> $(ENV_FILE)
	@echo "PROCESSOR_PORT=8001" >> $(ENV_FILE)
	@echo "[.env generated]"

env: $(ENV_FILE)
	@cat $(ENV_FILE)

build:
	docker build -t wiki-producer:latest wiki_producer/
	docker build -t wiki-processor:latest wiki_stream_processor/

push:
	docker tag wiki-producer:latest $(DOCKER_REGISTRY)/wiki-producer:latest
	docker tag wiki-processor:latest $(DOCKER_REGISTRY)/wiki-processor:latest
	docker push $(DOCKER_REGISTRY)/wiki-producer:latest
	docker push $(DOCKER_REGISTRY)/wiki-processor:latest

start:
	minikube start --driver=docker --memory=4096 --cpus=2 --force --no-vtx-check
	-minikube addons disable dashboard || true
	-minikube addons disable storage-provisioner || true

stop:
	minikube stop

ip:
	@echo "Minikube IP: $$(minikube ip)"

deploy: env
	kubectl apply -f $(K8S_DIR)/

delete:
	kubectl delete -f $(K8S_DIR)/ || true

helm-install:
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo update
	helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
		--namespace default \
		-f helm/prometheus-kube-prometheus-stack-values.yaml

helm-uninstall:
	helm uninstall prometheus || true

port-forward-kafka-ui:
	kubectl port-forward service/kafka-ui $(KAFKA_UI_PORT):8080

port-forward-kibana:
	kubectl port-forward service/kibana $(KIBANA_PORT):5601

port-forward-prometheus:
	kubectl port-forward svc/prometheus-kube-prometheus-prometheus $(PROM_PORT):9090

port-forward-grafana:
	kubectl port-forward svc/prometheus-grafana $(GRAFANA_PORT):80

dashboard:
	@echo "Kafka UI:       http://localhost:$(KAFKA_UI_PORT)"
	@echo "Kibana:         http://localhost:$(KIBANA_PORT)"
	@echo "Prometheus:     http://localhost:$(PROM_PORT)"
	@echo "Grafana:        http://localhost:$(GRAFANA_PORT)"

open-dashboard:
	cmd /c start http://localhost:$(KAFKA_UI_PORT)
	cmd /c start http://localhost:$(KIBANA_PORT)
	cmd /c start http://localhost:$(PROM_PORT)
	cmd /c start http://localhost:$(GRAFANA_PORT)

metrics:
	kubectl top pods --all-namespaces || echo "metrics-server not enabled"

logs:
	kubectl logs -l app=wiki-producer --tail=100 -f &
	kubectl logs -l app=wiki-processor --tail=100 -f

logs-producer:
	kubectl logs -l app=wiki-producer --tail=100 -f

logs-processor:
	kubectl logs -l app=wiki-processor --tail=100 -f

reset: delete helm-uninstall
	minikube delete --all --purge
	docker rmi wiki-producer:latest wiki-processor:latest || true
	@rm -f $(ENV_FILE)

help:
	@echo ""
	@echo "📦 Makefile Commands:"
	@echo "----------------------------------------"
	@echo " start               - Start Minikube (Docker driver)"
	@echo " stop                - Stop Minikube"
	@echo " ip                  - Show Minikube IP"
	@echo " env                 - Generate and print .env file"
	@echo " build               - Build Docker images"
	@echo " push                - Push images to registry"
	@echo " deploy              - Apply all K8s manifests"
	@echo " delete              - Delete all K8s resources"
	@echo " helm-install        - Install Prometheus/Grafana stack"
	@echo " helm-uninstall      - Uninstall Prometheus stack"
	@echo " port-forward-*      - Forward ports for services"
	@echo " dashboard           - Print dashboard URLs"
	@echo " open-dashboard      - Open all dashboards in browser"
	@echo " metrics             - Show cluster metrics"
	@echo " logs                - Logs from producer + processor"
	@echo " logs-producer       - Logs from producer only"
	@echo " logs-processor      - Logs from processor only"
	@echo " reset               - Full cleanup (K8s, Docker, .env)"
	@echo " help                - Show this help menu"
	@echo "----------------------------------------"
