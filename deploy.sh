#!/bin/bash
set -e

# Run commands on tafelberg-api.samtx.dev server with ssh

run_on_server () {
    ssh sam@tafelberg-api.samtx.dev "cd /opt/tafelberg-api && $1"
}

echo "Connect to tafelberg-api.samtx:/opt/tafelberg-api"

echo "check pwd"
run_on_server "pwd"

echo "Pull latest commit"
run_on_server "git pull"

echo "Build docker image"
run_on_server "docker build -t tafelberg-api:latest ."

echo "Run tests"
run_on_server "docker run tafelberg-api bash -c 'pip install --user pytest pytest-asyncio && pytest'"

echo "Stop current running container"
run_on_server "docker stop tafelberg-api || true"

echo "Remove named container"
run_on_server "docker rm tafelberg-api || true"

echo "Run new container image"
run_on_server "docker run -d \
    --name tafelberg-api \
    -p 8000:8000 \
    --log-driver=local \
    --restart=unless-stopped \
    tafelberg-api:latest
"