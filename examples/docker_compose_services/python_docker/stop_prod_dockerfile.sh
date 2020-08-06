#!/bin/bash

#
# This is an example on how to stop the currently running,
# and detached `run_prod_dockerfile.sh`
#

echo "Stopping Docker Container Named 'python_docker_example_container'"
sudo docker stop python_docker_example_container

echo "Removing  Docker Container Named 'python_docker_example_container'"
sudo docker rm python_docker_example_container
