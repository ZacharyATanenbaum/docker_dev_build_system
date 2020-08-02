
## [Docker Developer Build System](https://pypi.org/project/ddbs)

This system is used to inject a developer environment into a
docker compose system.
This will allow a developer to have one definition of their, say python, developer environment and have it setup perfectly for each Docker service.

This will allow new developers to quickly develop on new services, new machines and with new languages without "gumming up" their local disk.


### Dependencies

This library requires the following dependencies...
1. Docker Compose
2. Docker
3. Python3


### Install

To install run the following command either in your global python environment or a virtual environment.
```
python3 -m pip3 install ddbs
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
If one installed the `ddbs` within a virtual environment they must start that virtual environment before running the following command.
```
python3 -m ddbs -s $SERVICE_NAME -p $PERSONAL_DEV_ENIVRONMENT_BASE_PATH
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

### Troubleshooting/FAQ

#### Help! What are all these .autogenerated and .bin/ files?

Well, these files are generated automatically for this script to function.
By default the following files are autogenerated:
- `./<service_name>/.Dockerfile.autogenerated`
  - This is used as the "Dockerfile" for the development mode.
  - This file has both the Dockerfile.development and personally provided dockerfile commands.
- `./.docker-compose.autogenerated`
  - This is used as the "docker-compose.yml" for the development mode.
  - This file is the original "docker-compose.yml" file with the personal provided docker-compose commands injected for the provided service name.
- `./.start_dev.autogenerated`
  - This is used as a "start\_docker\_compose.sh" script.
  - This file is used to automatically run the commands in the `personal_run_commands.sh` file.
- `./<service_name>/.bin/`
  - This file is used for any needed files for "Dockerfile" build time.
  - This can be used to copy a script into a development environment.

To get rid of these from a git repo - it's recommended to add the following to your `.gitignore`:
- `*.autogenerated`
- `.bin/`

#### Why don't you remove the .autogenerated and .bin/ files automatically?

Well, these files can be removed automatically.
But, having them persist allows for easier debugging, quick checking for another developer (to mimic) or quick checking of the current configuration by the current developer.
Additionally, it would be quite complex to add code to remove these files _during_ development and they're needed to start development.
It would be easy to remove them after development... but then a developer would already have "seen" them via git.

Thus, they stay.
