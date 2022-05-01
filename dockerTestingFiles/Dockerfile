FROM python:3.9-alpine

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13

# Add Compiler
RUN apk add -U --no-cache gcc build-base linux-headers ca-certificates python3-dev libffi-dev libressl-dev libxslt-dev

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY ClubSeek/poetry.lock ClubSeek/pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production) --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY ClubSeek /

# Add Label to Docker Image (test)
LABEL org.opencontainers.image.source https://github.com/radical-teach/major-project-group-4


