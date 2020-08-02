#!/bin/bash

# Used to setup git within container
export GIT_USER_EMAIL=$(git config user.email)
export GIT_USER_NAME=$(git config user.name)
export HOST_GROUP_ID=$(id -g $USER)
export HOST_USER_ID=$(id -u $USER)

sudo -E docker-compose \
    -f {dev_docker_compose_filename} \
    down \
    --remove-orphans

sudo -E docker-compose \
    -f {dev_docker_compose_filename} \
    build \
    --no-cache

sudo -E docker-compose \
    -f {dev_docker_compose_filename} \
    run \
    --service-ports \
    {service_name} \
    /opt/setup_image.sh
