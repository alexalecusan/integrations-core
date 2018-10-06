# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from .docker import DockerInterface
from .run import start_environment, stop_environment


def get_interface(metadata):
    env_type = metadata.get('env_type', 'docker')

    if env_type == 'docker':
        return DockerInterface
