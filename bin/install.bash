#!/usr/bin/env bash

docker-compose up -d
docker-compose exec app invoke populate

echo "Ensure domain names of URL map returned by the last command resolv to 127.0.0.1"

docker-compose exec app invoke run
