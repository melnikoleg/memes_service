FROM python:3.9.6-slim-buster
RUN apt-get update && apt-get install -y --reinstall build-essential \
  gcc supervisor\
   && rm -rf /var/lib/apt/lists/*
EXPOSE 8000

RUN pip install poetry==1.2.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements

RUN poetry install

# Copying actuall application
COPY . /app/src/
RUN poetry install

#CMD ["/usr/local/bin/python", "-m", "memes_service"]
