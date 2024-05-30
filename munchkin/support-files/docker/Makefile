start-dev:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml up -d

stop-dev:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml down

dev-logs:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml logs -f

remove-all-volume:
	docker volume rm $(docker volume ls -q)

create-network:
	docker network create traefik