FROM python:3.9-slim-buster

WORKDIR /app

# Install poetry:
RUN pip install poetry

# Copy in the config files:
COPY ClubSeek/pyproject.toml ClubSeek/poetry.lock ./
# Install only dependencies:
RUN poetry install --no-root 

# Copy in everything else and install:
COPY /ClubSeek .
RUN poetry install 

CMD [ "poetry" , "run" , "python" , "clubseek/main.py"]