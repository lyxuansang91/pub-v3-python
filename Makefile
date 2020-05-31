TEKO_REGISTRY := hub.teko.vn
IMAGE_NAME := identity-admin-api
DEVELOP_TAG := develop

IMAGE_DEV := $(DOCKER_USERNAME)/$(IMAGE_NAME):$(DEVELOP_TAG)

teko-docker-login:
	@echo "$(TEKO_PASSWORD)" | docker login $(TEKO_REGISTRY) -u $(TEKO_USERNAME) --password-stdin 

docker-login:
	@echo "$(DOCKER_PASSWORD)" | docker login -u $(DOCKER_USERNAME) --password-stdin

build-image:
	docker build --cache-from  $(IMAGE_DEV) -t $(IMAGE_DEV) .

push-image:
	docker push $(IMAGE_DEV)