build:
	docker-compose build

up:
	docker-compose up

test:
	docker-compose exec app coverage run -m pytest && docker-compose exec app coverage report -m

logs:
	docker-compose logs app | tail -100

down:
	docker-compose down

all: down build up test
