# Makefile for Wiki_Kafka_Kind Pipeline

# Project Variables
KIND_CLUSTER_NAME=wiki-kafka-cluster
KUBECTL=kubectl
KIND=kind
MANIFEST_DIR=manifests
NAMESPACE=default

.PHONY: help create-cluster delete-cluster deploy logs producer-logs processor-logs port-forward-kibana port-forward-kafka-ui destroy

help:
	@echo "Wiki_Kafka_Kind Project Commands:"
	@echo " make create-cluster    - Create KIND cluster"
	@echo " make delete-cluster    - Delete KIND cluster"
	@echo " make deploy            - Apply Kubernetes manifests"
	@echo " make logs              - View all pod logs"
	@echo " make producer-logs     - View wiki-producer logs"
	@echo " make processor-logs    - View wiki-processor logs"
	@echo " make port-forward-kibana - Access Kibana UI locally"
	@echo " make port-forward-kafka-ui - Access Kafka UI locally"
	@echo " make destroy           - Teardown everything"

create-cluster:
	$(KIND) create cluster --name $(KIND_CLUSTER_NAME)

delete-cluster:
	$(KIND) delete cluster --name $(KIND_CLUSTER_NAME)

deploy:
	$(KUBECTL) apply -f $(MANIFEST_DIR)/

pods:
	$(KUBECTL) get pods

logs:
	$(KUBECTL) logs -l app=wiki-producer --tail=100 -f &
	$(KUBECTL) logs -l app=wiki-processor --tail=100 -f &

producer-logs:
	$(KUBECTL) logs deployment/wiki-producer -f

processor-logs:
	$(KUBECTL) logs deployment/wiki-processor -f

port-forward-kibana:
	$(KUBECTL) port-forward service/kibana 5601:5601

port-forward-kafka-ui:
	$(KUBECTL) port-forward service/kafka-ui 9000:8080

destroy:
	$(KUBECTL) delete -f $(MANIFEST_DIR)/
	$(KIND) delete cluster --name $(KIND_CLUSTER_NAME)
