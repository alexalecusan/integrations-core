# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from .config import locate_config_file, locate_env_dir, write_env_data
from ...subprocess import run_command
from ...utils import remove_path


class DockerInterface(object):
    def __init__(self, check, env, config=None, metadata=None):
        self.check = check
        self.env = env
        self.config = config or {}
        self.metadata = metadata or {}

    def locate_config(self):
        return locate_config_file(self.check, self.env)

    def remove_config(self):
        remove_path(locate_env_dir(self.check, self.env))

    def write_config(self):
        write_env_data(self.check, self.env, self.config, self.metadata)

    def start_agent(self):
        pass

    def stop_agent(self):
        pass


def get_docker_networks():
    command = ['docker', 'network', 'ls', '--format', '{{.Name}}']
    lines = run_command(command, capture='out', check=True).stdout.splitlines()

    return [line.strip() for line in lines]
