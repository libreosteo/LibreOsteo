TAG := latest 
HOST_PORT := 8085
GUEST_PORT := 8085
REPOSITORY := libreosteo
APP := libreosteo
help:
	@echo "Building LibreOsteo docker image"

build: build-http-ready build-sock-ready

build-http-ready:
	@echo "Build LibreOsteo app (Http ready)"
	docker buildx build --platform=linux/amd64,linux/arm64,linux/arm -f Docker/build/http-ready/Dockerfile . -t $(REPOSITORY)/$(APP)-http:$(TAG) --push

build-sock-ready:
	@echo "Build LibreOsteo app (Sock ready)"
	docker buildx build --platform=linux/amd64,linux/arm64,linux/arm -f Docker/build/sock-ready/Dockerfile . -t $(REPOSITORY)/$(APP)-sock:$(TAG) --push

build-postgres:
	@echo "Build Postgresql (for libreosteo)"
	docker build --progress=plain -f Docker/build/postgresql/Dockerfile . -t $(REPOSITORY)/$(APP)-pg:${TAG} --output type=docker 

run:
	docker run -d --rm --name $(APP)_app -p $(HOST_PORT):$(GUEST_PORT) --mount source=libreosteo-data,target=/Libreosteo/data --mount source=libreosteo-settings,target=/Libreosteo/settings $(REPOSITORY)/$(APP)-http:$(TAG)

run-pg:
	docker-compose --env-file=.env -f Docker/deploy/pg/docker-compose.yml up

.DEFAULT_GOAL := help
