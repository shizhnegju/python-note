NAME=rock

base:
	echo build ${NAME}:base
	cp docker/be/base/Dockerfile .
	docker build -t ${NAME}:base .
	rm Dockerfile


build: base
	echo build ${NAME}:prod
	cp docker/be/prod/Dockerfile .
	docker build -t ${NAME}:prod .
	rm Dockerfile

be-build:
	echo build ${NAME}:prod
	cp docker/be/prod/Dockerfile .
	docker build -t ${NAME}:prod .
	rm Dockerfile

dev:
	docker-compose up -d

down:
	docker-compose down