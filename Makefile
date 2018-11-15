.PHONY: help

# CONFIG
PORT = 5000
DOCKER_IMAGE = "kungalex/rest-mqtt-proxy"
DOCKER_TAG = "latest"
APP_NAME = "rest-mqtt-proxy"

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build Container-Image
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

build-nc: ## Build Container-Image without caching
	docker build --no-cache -t kungalex/$(APP_NAME) .

run: ## Run Container
	docker run -it -p=$(PORT):5000 --name="$(APP_NAME)" $(APP_NAME)

stop: ## Stop and remove Container
	docker stop $(APP_NAME); docker rm $(APP_NAME)

release: build-nc publish ## Release Container-Image (build and publish)

publish: ## Publish Container-Image
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)



