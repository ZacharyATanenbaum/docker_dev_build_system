#!/bin/bash

#
# This is an example on how to run this specific docker
# program without compose.
#

echo "Building Image 'python_docker_example'"
sudo docker build --tag python_docker_example .

echo "Running Image 'python_docker_example' with name 'python_docker_example_container'"
sudo docker run \
    --publish 8000:8080 \
    --name python_docker_example_container \
    python_docker_example
