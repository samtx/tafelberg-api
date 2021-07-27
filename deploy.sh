#!/bin/bash

echo "Pull latest commit"
git pull

echo "Build docker image"
docker build -t tafelberg-api:latest .

echo "Stop current running container"
docker stop tafelberg-api || true

echo "Remove named container"
docker rm tafelberg-api || true

echo "Run new container image"
docker run -d \
    --name tafelberg-api \
    -p 8000:8000 \
    --log-driver=local \
    --restart=unless-stopped \
    tafelberg-api:latest