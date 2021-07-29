#!/bin/bash
set -e

docker run tafelberg-api pip install --user pytest pytest-asyncio && pytest