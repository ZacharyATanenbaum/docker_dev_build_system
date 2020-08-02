
## Docker Developer Build System

This system is used to inject a developer environment into a
docker compose system.


### Dependencies

This library requires the following dependencies...
1. Docker Compose
2. Docker
3. Python3


### Install

To install run the following command either in your global python environment or a virtual environment.
```
python3 -m pip3 install docker_dev
```


### Project Prerequisites

The project to have a development environment injected must have the following:
1. docker-compose.yml
2. Dockerfile (For the service to run in development mode)
3. Dockerfile.development (For the service to run in development mode)
  - This file will be all the commands to setup the service in a development mode.


### Personal Prerequisites

Some files must be provided to create the proper development environment.
Below will list the provided files for a creating a personal development environment that will be inject into the docker service.
If you're a sane person the [x11docker](https://github.com/mviereck/x11docker) image can be used to run IDE's within a container.
Additionally, feel free to check out the [./examples/personal\_setup/](./examples/personal_setup/) folder to see an example for personal configuration.

Files Needed:
1. `personal_docker_compose_commands.yml`
2. `personal_dockerfile_commands.txt`
3. `personal_run_commands.sh`

Optional Files:
1. `./bin/`

#### personal\_docker\_compose\_commands.yml

This file is used to inject docker\_compose commands.
This file is combined with the specific commands for the provided service to create a new docker\_compose file.

#### personcal\_dockerfile\_commands.txt

This is all of the Dockerfile commands that should be added to the development environment.
These commands will be combined with the provided `Dockerfile.development` to create the specific development environment.
__NOTE:__ Dockerfile commands will NOT overwrite the provided commands. So make sure to set the image/use the `FROM` command in only one file.

#### personal\_run\_commands.sh

This is the file that will be run to trigger the development `docker-compose.yml` file.
Please provide a `-f {dev_docker_compose_filename}` to the run command as well as `{service_name}` for the target.
The system will automatically fill in these values with the development docker compose file (for `dev_docker_compose_filename`) and the service name that will be run in development mode.

#### ./bin/

Everything in this directory will be moved to the `./.bin/` (__NOTE: That's a hidden file__) in the same directory of the development Dockerfile.
Thus, if one needs to have file available at Dockerfile creation time they can be placed in this folder.


### Running

#### Command

Use the following command to run the service.
If one installed the `docker_dev` within a virtual environment they must start that virtual environment before running the following command.
```
python3 -m docker_dev -s $SERVICE_NAME -p $PERSONAL_DEV_ENIVRONMENT_BASE_PATH
```

#### Required Arguments
##### Service Name

This is the service that will be started within the development environment.
This must be the same name as the service is within the production `docker-compose.yml` file.
```
-s
--service
```

##### Personal Dev Environment Base Path

This is the base (__absolute__) path to the base folder that holds all the fun files/folders defined within the _Personal Prerequisites_ section.
```
-p
--personal
```
