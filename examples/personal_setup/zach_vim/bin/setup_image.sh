#!/bin/bash

# This is run WITHIN the docker container
echo "STARTING ALL THE THINGS!"

# Setup git config of the user within the docker container to be
# the same as the provided environment variables.
if [ ! -z "$GIT_USER_NAME" ] && [ ! -z "$GIT_USER_EMAIL" ]; then
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
fi

# Setup SSH Agent for Git within the docker container.
eval "$(ssh-agent -s)"
ssh-add /etc/ssh/id_rsa

# Install Vundle Plugins for the user within the docker container.
vim +PluginInstall +qall

# Start Tmux + allow actual interactions!
tmux
