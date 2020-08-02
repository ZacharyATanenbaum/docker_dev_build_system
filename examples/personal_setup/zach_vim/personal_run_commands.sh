#!/bin/bash

# Used to setup git within container
export GIT_USER_EMAIL=$(git config user.email)
export GIT_USER_NAME=$(git config user.name)
export HOST_GROUP_ID=$(id -g $USER)
export HOST_USER_ID=$(id -u $USER)

# Turn off any straggling containers
sudo -E docker-compose \
    -f {dev_docker_compose_filename} \
    down \
    --remove-orphans

# Re-build without cache to pickup all Dockerfile changes
sudo -E docker-compose \
    -f {dev_docker_compose_filename} \
    build \
    --no-cache

# Run the thing while opening ports locally
sudo -E docker-compose \
    -f {dev_docker_compose_filename} \
    run \
    --service-ports \
    {service_name} \
    /opt/setup_image.sh
