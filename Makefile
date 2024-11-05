stop:
	sudo docker compose down

run:
	sudo docker compose up --build web nginx db

db.shell:
	sudo docker exec -it db bash

run.test_app:
	sudo docker compose up -d test_web

test: run.test_app
	sudo docker exec -it test_web sh -c "poetry run pytest . -vv"

test.coverage: run.test_app
	sudo docker exec -it test_web sh -c "poetry run pytest --cov-report term --cov=app . -vv"

build.web:
	sudo docker compose build web

lint: build.web
	sudo docker run --rm adastra_task-web sh -c "poetry run black --color . && poetry run ruff check --fix && poetry run mypy . && poetry run codespell --enable-colors /app && poetry run refurb ."