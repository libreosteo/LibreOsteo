TAG := latest
HOST_PORT := 8085
GUEST_PORT := 8085
help:
	@echo "Building LibreOsteo docker image"

build: build-http-ready build-sock-ready

build-http-ready:
	@echo "Build LibreOsteo app (Http ready)"
	docker build -f Docker/build/http-ready/Dockerfile . -t libreosteo-http:$(TAG)

build-sock-ready:
	@echo "Build LibreOsteo app (Sock ready)"
	docker build -f Docker/build/sock-ready/Dockerfile . -t libreosteo-sock:$(TAG)

build-postgres:
	@echo "Build Postgresql (for libreosteo)"
	docker build -f Docker/build/postgresql/Dockerfile . -t libreosteo-pg:${TAG}

run:
	docker run -d --rm --name libreosteo_app -p $(HOST_PORT):$(GUEST_PORT) --mount source=libreosteo-data,target=/data --mount source=libreosteo-settings,target=/settings libreosteo-http:$(TAG)

run-pg:
	docker-compose --env-file=.env -f Docker/deploy/pg/docker-compose.yml up

.DEFAULT_GOAL := help
