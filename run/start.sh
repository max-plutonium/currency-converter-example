#! /bin/bash

echo "Start the API"
echo "tag: \"${IMAGE_TAG}\", rev: ${GIT_COMMIT}"

exec uvicorn app.application:server --workers 1 "$@"
