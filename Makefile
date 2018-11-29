.PHONY: help

# CONFIG
PORT = 5000
DOCKER_IMAGE = "kungalex/rest-mqtt-proxy"
DOCKER_TAG = "latest"
APP_NAME = "rest-mqtt-proxy"

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


test: ## Run unit tests
	echo "not implemented now"

build: ## Build Container-Image
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

build-nc: ## Build Container-Image without caching
	docker build --no-cache -t kungalex/$(APP_NAME) .

build-docs: ## rebuild documentation
	echo "not implemented now"

run: ## Run Container
	docker run -it \
	--name="$(APP_NAME)" \
	-p=$(PORT):5000 \
    -e APP_CONFIG_FILE=/srv/rest-mqtt-proxy/config.ini \
    -e PRE_MAPPING_DIR=/srv/rest-mqtt-proxy/mappings \
    -v ${PWD}/config/dev/config.ini:/srv/rest-mqtt-proxy/config.ini:ro \
    -v ${PWD}/config/dev/mappings/:/srv/rest-mqtt-proxy/mappings/:ro \
    $(DOCKER_IMAGE):$(DOCKER_TAG)

run-prod: ## Run Container
	docker run -it \
	--name="$(APP_NAME)" \
	-p=$(PORT):5000 \
    -e APP_CONFIG_FILE=/srv/rest-mqtt-proxy/config.ini \
    -e PRE_MAPPING_DIR=/srv/rest-mqtt-proxy/mappings \
    -v ${PWD}/config/prod/config.ini:/srv/rest-mqtt-proxy/config.ini:ro \
    -v ${PWD}/config/prod/mappings/:/srv/rest-mqtt-proxy/mappings/:ro \
    $(DOCKER_IMAGE):$(DOCKER_TAG)

test-config-dev: ## Test Config and Pre-Mappings files develop Env
	docker run -it \
    -e APP_CONFIG_FILE=/srv/rest-mqtt-proxy/config.ini \
    -e PRE_MAPPING_DIR=/srv/rest-mqtt-proxy/mappings \
    -v ${PWD}/config/dev/config.ini:/srv/rest-mqtt-proxy/config.ini:ro \
    -v ${PWD}/config/dev/mappings/:/srv/rest-mqtt-proxy/mappings/:ro \
    $(DOCKER_IMAGE):$(DOCKER_TAG) python config-test.py

test-config-prod: ## Test Config and Pre-Mappings files for production Env
	docker run -it \
    -e APP_CONFIG_FILE=/srv/rest-mqtt-proxy/config.ini \
    -e PRE_MAPPING_DIR=/srv/rest-mqtt-proxy/mappings \
    -v ${PWD}/config/prod/config.ini:/srv/rest-mqtt-proxy/config.ini:ro \
    -v ${PWD}/config/prod/mappings/:/srv/rest-mqtt-proxy/mappings/:ro \
    $(DOCKER_IMAGE):$(DOCKER_TAG) python config-test.py

up: build run ## Build and Run Container

check-config-dev: build-nc test-config-dev ## Build without caching and test develop config

check-config-prod: build-nc test-config-prod ## Build without caching and test production config

stop: ## Stop and remove Container
	docker stop $(APP_NAME); docker rm $(APP_NAME)

release: build-nc publish ## Release Container-Image (build and publish)

publish: ## Publish Container-Image
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)

compose-dev: ## Develop Docker-compose up
	docker-compose up

compose-prod: ## Production Docker-compose up
	docker-compose -f docker-compose-prod.yaml  up

