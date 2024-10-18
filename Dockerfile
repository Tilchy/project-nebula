FROM python:3.13-slim

RUN python -m pip install --upgrade pipx

RUN pipx install poetry

RUN apt-get update && apt-get install -y git

WORKDIR /app

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app

COPY pyproject.toml /app
COPY poetry.lock /app
COPY ./src /app/src
COPY run.sh /app

RUN poetry install --no-interaction --no-root
RUN chmod +x /app/run.sh

EXPOSE 8000

ENTRYPOINT ["/app/run.sh"]