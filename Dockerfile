FROM python:3.9-slim

ARG ENVIRONMENT

ENV ENVIRONMENT=${ENVIRONMENT}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.1

RUN apt-get update

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
  && poetry install $([ "$ENVIRONMENT" == production && echo "--no-dev" ]) --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY src .
