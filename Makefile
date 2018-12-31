CONTAINER=flaskapp

.PHONY: up

dev :
	python3 app/main.py

validate :
	docker-compose config

build : validate
	docker-compose build

rm :
	docker rmi `docker images | awk "{print $3}"`

rm_exited :
	docker rm `docker ps -aqf status=exited`

rm_images_dangling :
	docker rmi `docker images --filter "dangling=true" -q --no-trunc`

pull :
	docker-compose pull

up : pull
	docker-compose up -d

down :
	docker-compose down

restart :
	docker-compose restart

reset : down
	make up

shell :
	docker exec -ti $(CONTAINER) /bin/bash

service:
	cp docker-compose-fmmss.service /etc/systemd/system/docker-compose-fmmss.service
	systemctl enable docker-compose-fmmss
