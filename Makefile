stop:
	docker compose down

run:
	docker compose up --build web nginx db

restart: stop run

db.shell:
	docker exec -it db sh -c "psql -Upostgres"

run.test_app:
	docker compose up -d test_web

test: run.test_app
	docker exec -it test_web sh -c "poetry run pytest . -vv"

test.coverage: run.test_app
	docker exec -it test_web sh -c "poetry run pytest --cov-report term --cov=app . -vv"

build.web:
	docker compose build web

lint: build.web
	docker run --rm adastra_task-web sh -c "poetry run isort . && poetry run black --color . && poetry run ruff check --fix && poetry run mypy . && poetry run codespell --enable-colors /app && poetry run refurb ."