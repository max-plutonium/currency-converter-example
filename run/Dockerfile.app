FROM python:3.9-slim

MAINTAINER Max Plutonium <plutonium.max@gmail.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
    aptitude bash curl libffi-dev libssl-dev openssl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 - && \
    poetry config virtualenvs.create false

WORKDIR /app/

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PYCURL_SSL_LIBRARY openssl

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

RUN aptitude install -y --add-user-tag .build-deps \
    make gcc git libcurl4-openssl-dev cargo && \
    python -m pip install --upgrade pip && \
    poetry install --no-root --only main && \
    aptitude purge -y '?user-tag(.build-deps)'

COPY app /app/app
COPY run/start.sh /app/

RUN chmod +x /app/start.sh

ARG GIT_COMMIT=dev
ARG IMAGE_TAG=dev

ENV GIT_COMMIT $GIT_COMMIT
ENV IMAGE_TAG $IMAGE_TAG

RUN touch /~build.rev.${GIT_COMMIT}.txt && touch /~build.tag.${IMAGE_TAG}.txt \
    touch /~build.date.`date '+%F_%H:%M:%S'`.txt

RUN echo "Built rev: ${GIT_COMMIT}"

EXPOSE 80

ENTRYPOINT ["/app/start.sh"]
