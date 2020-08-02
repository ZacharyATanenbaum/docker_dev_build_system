
## Docker Compose Services

---
### Overview

Exactly as the name states.
This is a repo of Dockerized services that uses Docker Compose!

In general it's two services that are pretty straightforward...
- A Flask Python App
- A Redis Database

The Flask Python App, or `python_docker`, will start a Flask webservice on localhost port 5000 (`localhost:5000`).
Whenever this endpoint is hit it will return the number of times it's been hit.
This data is persisted in a Redis database, or `redis`, and that data should be saved under the `./redis-data` folder.


---
### Dependencies

- Docker
- Docker-Compose
- Python
- [docker\_dev (This Repo...)](https://github.com/ZacharyATanenbaum/docker_dev_build_system)


---
### Running the System

#### Production

To run the system in production is a pretty straightforward and regular `docker-compose` program.
To make it easier (as the containers will conflict with the "development" containers there's a script `run_production.sh` that will make sure to re-build everything prior to running production.

#### Development

Running in development is where stuff gets interesting.
To launch "development mode" run the `start_development.sh` script.

__Yes__ this will ask you for `sudo` power.
__No__ this will not harm your computer.
Sudo is needed to run [the proper docker-compose commands in this file (../personal\_setup/zach\_vim/personal\_run\_commands.sh)](../personal_setup/zach_vim/personal_run_commands.sh)
Which is what automatically starts docker-compose.

Once `start_development.sh` is run it will:
- Trigger this lovely `docker_dev` package.
- Stop all running servies with the same names as those dictated in the `docker-compose.yml`.
- Build all of the services located in the `docker-compose.yml` file with `python_docker` in development mode.
- Start a `tmux` session in a "development" container for the `python_docker` service.

To start the `python_docker` itself run the `./python_docker/start_python_docker.sh` script.

To find a full list of how it's setup view the [../personal\_setup/zach\_vim/](../personal_setup/zach_vim/) folder and the [./python\_docker/Dockerfile.development](./python\_docker/Dockerfile.development) file.

A quick overview is as follows:
- `python_docker` setup under `/app/` and can be started w/ `start_production.sh`
- git (setup with the current user's configuration)
- vim (setup with the current user's configuration)
- tmux (default setup)
- dev user (setup with the current user's user id and group id)
- bash (setup with the current user's configuation)
- ssh (setup with the current user's configuration)
- Pylint
- Vundle (setup with the current user's vimrc)
- Vundle Plugins (again depending on the current user's vimrc)


---
### Troubleshooting / FAQ

#### Why does it build so slow?

The [../personal\_setup/zach\_vim/personal\_run\_commands.sh](../personal_setup/zach_vim/personal_run_commands.sh) has `--no-cache` under the build section.
This allows all changes to the setup scripts/personal setup to immediately reflect on the actual running image.
This also allows all changes to the Dockerfile.development to be picked up.
Thus, the 1x occurance of 30s (less than a lot of compile times!) build time is worth it.
Please feel free to remove `--no-cache` if you'd like and aren't going to be modifying the "personal setup".
