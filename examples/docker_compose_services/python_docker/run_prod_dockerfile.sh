#!/bin/bash

#
# This is an example on how to run this specific docker
# program without compose.
#

sudo docker build --tag python_docker_example .
sudo docker run \
    --publish 8000:8080 \
    --name python_docker_example_name \
    python_docker_example
