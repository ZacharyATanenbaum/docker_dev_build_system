""" Script to Build Dockerfiles and docker-compose.yml """

import argparse
import logging
import os
import shutil
import stat
import subprocess
import yaml

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    """
    Main method...
    """
    vargs = get_arguments()

    LOG.debug(f'Starting Environment for Service: "{vargs.service_name}"')
    LOG.debug(f'Getting Personal Dev Files from Path: "{vargs.personal}"')

    personal_developer_config = get_personal_config(vargs.personal)
    copy_bin_files(vargs.personal, vargs.service_folder)

    create_development_dockerfile(
        personal_developer_config['dockerfile_commands'],
        f'./{vargs.service_folder}/{vargs.service_dev_dockerfile_commands_filename}',
        f'./{vargs.service_folder}/{vargs.service_dev_dockerfile_filename}' 
    )

    create_development_docker_compose(
        vargs.service_name,
        vargs.service_folder,
        vargs.prod_docker_compose_filename,
        vargs.dev_docker_compose_filename,
        vargs.service_dev_dockerfile_filename,
        personal_developer_config['docker_compose_commands']
    )

    script_to_run = personal_developer_config['run_commands']
    script_to_run = script_to_run.format(
        service_name=vargs.service_name,
        dev_docker_compose_filename=vargs.dev_docker_compose_filename
    )
    run_docker_compose_command(
        script_to_run,
        vargs.start_development_script_name
    )


def copy_bin_files(absolute_base_personal_folder, relative_service_folder):
    """
    absolute_base_personal_folder::str 
    relative_service_folder::str
    """
    absolute_source_path = f'{absolute_base_personal_folder}/bin'
    relative_dest_path = f'{relative_service_folder}/.bin'

    if not os.path.isdir(absolute_source_path):
        LOG.warning(f'Cannot find "bin/" at "{absolute_source_path}" skipping...')
        return

    if os.path.isdir(relative_dest_path):
        shutil.rmtree(relative_dest_path)

    shutil.copytree(absolute_source_path, relative_dest_path)


def create_development_dockerfile(
        personal_dockerfile_commands,
        service_dev_dockerfile_commands_rel_path,
        service_dev_dockerfile_rel_path):
    """
    personal_dockerfile_commands::str
    service_dev_dockerfile_commands_path::str Commands to run the service in dev mode
    service_dev_dockerfile_path::str Output path for the dev dockerfile
    """
    with open(service_dev_dockerfile_commands_rel_path) as dockerfile_commands_file:
        provided_commands = dockerfile_commands_file.read()

    dev_dockerfile_commands = (
        '# AUTOGENERATED DO NOT OVERWRITE - Development Dockerfile\n'
        + provided_commands
        + personal_dockerfile_commands
    )

    with open(service_dev_dockerfile_rel_path, 'w') as dev_dockerfile:
        LOG.debug('Writing Dev Dockerfile:\n{}', dev_dockerfile_commands)
        dev_dockerfile.write(dev_dockerfile_commands)


def create_development_docker_compose(
        service_name,
        service_folder,
        prod_docker_compose_filename,
        dev_docker_compose_filename,
        service_dev_dockerfile_filename,
        personal_docker_compose_commands):
    """
    service_name::str
    service_folder::str
    prod_docker_compose_filename::str
    dev_docker_compose_filename::str
    service_dev_dockerfile_filename::str
    personal_docker_compose_commands::str Docker Compose Commands to be injected
    """
    with open(prod_docker_compose_filename, 'r') as prod_docker_compose:
        docker_compose = yaml.safe_load(prod_docker_compose)

    merge_dicts(
        docker_compose['services'][service_name],
        personal_docker_compose_commands
    )

    docker_compose['services'][service_name]['build'] = {
        'context': service_folder,
        'dockerfile': service_dev_dockerfile_filename
    }

    # Inject App Volume
    #git_folder_root_directory = subprocess.check_output(
    #    ['git', 'rev-parse', '--show-toplevel']
    #    ).decode('utf-8').strip()

    if 'volumes' not in docker_compose['services'][service_name]:
        docker_compose['services'][service_name]['volumes']

    #docker_compose['services'][service_name]['volumes'] += [f'{git_folder_root_directory}:/app/']
    docker_compose['services'][service_name]['volumes'] += [f'./{service_folder}:/app/']
    # Inject App Volume

    with open(dev_docker_compose_filename, 'w') as dev_docker_compose:
        LOG.debug('Writing Dev Docker Compose:\n{}', docker_compose)
        yaml.dump(docker_compose, dev_docker_compose)

    with open(dev_docker_compose_filename, 'a') as dev_docker_compose:
        dev_docker_compose.seek(0, 0)
        dev_docker_compose.write(
            '# AUTOGENERATED DO NOT OVERWRITE - Dev. Docker Compose\n'
        )


def get_arguments():
    """
    Get vargs
    """
    parser = argparse.ArgumentParser(
            description='Make and run docker-compose as development for a service'
    )

    # Required
    parser.add_argument(
        '-s',
        '--service_name',
        help='The name of the service to run in development mode'
    )
    parser.add_argument(
        '-p',
        '--personal',
        help='Personal development environment base folder path (absolute)'
    )

    # Optional
    parser.add_argument(
        '--service_folder',
        default=None,
        help='Folder for the service - defaults to "service_name" arg'
    )
    parser.add_argument(
        '--service_dev_dockerfile_commands_filename',
        default='Dockerfile.development',
        help="Filename for service's dockerfile comamnds"
    )
    parser.add_argument(
        '--service_dev_dockerfile_filename',
        default='.Dockerfile.autogenerated',
        help="Output Filename for the service's development dockerfile"
    )
    parser.add_argument(
        '--prod_docker_compose_filename',
        default='docker-compose.yml',
        help='Production Docker Compose filename'
    )
    parser.add_argument(
        '--dev_docker_compose_filename',
        default='.docker-compose.autogenerated',
        help='Production Docker Compose filename'
    )
    parser.add_argument(
        '--start_development_script_name',
        default='.start_dev.autogenerated',
        help='Production Docker Compose filename'
    )

    args = parser.parse_args()

    args.service_folder = (
        args.service_folder if args.service_folder else args.service_name
    )
    return args


def get_personal_config(absolute_config_path):
    """
    absolute_config_path::str
    return = {
        'dockerfile_commands'::str Dockerfile commands to inject
        'docker_compose_commands'::{} Parsed yaml for docker-compose injection
        'run_commands'::str Commands to run the docker-compose file
    }
    """
    path = f'{absolute_config_path}/personal_dockerfile_commands.txt' 
    with open(path, 'r') as dockerfile_file:
        dockerfile_commands = dockerfile_file.read()

    path = f'{absolute_config_path}/personal_docker_compose_commands.yml'
    with open(path, 'r') as docker_compose_file:
        docker_compose_commands = yaml.safe_load(docker_compose_file)

    path = f'{absolute_config_path}/personal_run_commands.sh'
    with open(path, 'r') as run_file:
        run_commands = run_file.read()

    return {
        'dockerfile_commands': dockerfile_commands,
        'docker_compose_commands': docker_compose_commands,
        'run_commands': run_commands
    }


def merge_dicts(target_dict, source_dict):
    """
    Merge the top layer of the source dict onto the target dict in place.
    target_dict::{} Dictionary to populate
    source_dict::{} Dictionary to take values from
    return::{} Combined dictionary
    """
    for key, value in source_dict.items():
        if key not in target_dict:
            target_dict[key] = value

        elif isinstance(target_dict[key], dict):
            merge_dicts(target_dict[key], value)

        elif isinstance(target_dict[key], list):
            to_add = []

            for item in value:
                if item not in target_dict[key]:
                    to_add.append(item)

            target_dict[key] += to_add

        elif key in target_dict:
            LOG.warning(f'Overwritting: {key} with {value}')
            target_dict[key] = value

        else:
            raise RuntimeError(f'Unable to put {key} and {value} into target dict...')


def run_docker_compose_command(commands, dev_script_name):
    """
    commands::str
    dev_script_name::str
    """
    with open(dev_script_name, 'w') as dev_script_file:
        lines = commands.splitlines()
        lines.insert(1, '# AUTOGENERATED DO NOT OVERWRITE - Dev. Run Script\n')
        to_write = '\n'.join(lines)
        LOG.debug('Developer docker-compose.yml:\n %s', to_write)
        dev_script_file.write(to_write)

    try:
        os.chmod(dev_script_name, stat.S_IRWXU)
        subprocess.call([f'./{dev_script_name}'])
    finally:
        os.remove(dev_script_name)


if __name__ == '__main__':
    main()
