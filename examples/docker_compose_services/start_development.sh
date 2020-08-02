#/bin/bash

export PATH_TO_BASE_OF_GIT_REPO=$(git rev-parse --show-toplevel)
export PATH_TO_PERSONAL_SETUP='examples/personal_setup/zach_vim'
export PERSONAL_SETUP_PATH="$PATH_TO_BASE_OF_GIT_REPO/$PATH_TO_PERSONAL_SETUP"

python -m docker_dev \
    -s "python_docker" \
    -p $PERSONAL_SETUP_PATH
