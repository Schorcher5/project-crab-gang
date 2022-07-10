#!/bin/bash

# Move and activate script in parent folder in order for it to work properly


cd ./project-crab-gang
git fetch && git reset origin/main --hard
docker compose -f docker-compose-prod.yml down
docker compose -f docker-compose-prod.yml up -d --build
echo "testing"
