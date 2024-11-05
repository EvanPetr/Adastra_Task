FROM python:3.12.6-slim-bullseye

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

RUN apt-get -y update; apt-get -y install curl
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install --no-root --no-dev

COPY . /src

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
