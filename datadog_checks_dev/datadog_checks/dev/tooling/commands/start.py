# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import click

from .utils import CONTEXT_SETTINGS, abort, echo_failure, echo_info, echo_success, echo_waiting
from ..e2e import get_interface, start_environment, stop_environment
from ..test import get_available_tox_envs
from ..utils import get_tox_file
from ...utils import file_exists


@click.command(
    context_settings=CONTEXT_SETTINGS,
    short_help='Start an environment for a check'
)
@click.argument('check')
@click.argument('env', required=False)
@click.option('--list', '-l', 'list_envs', is_flag=True, help='List available environments')
def start(check, env, list_envs):
    """Start an environment for a check."""
    if not file_exists(get_tox_file(check)):
        abort('`{}` is not a testable check.'.format(check))

    envs = get_available_tox_envs(check, test_only=True)

    if list_envs:
        echo_success('`{}`:'.format(check))
        for e in envs:
            echo_info('    {}'.format(e))
        return

    if not env:
        echo_failure('You must select an environment.')
        echo_info('See what is available via `ddev start --list {}`.'.format(check))
        abort()

    if env not in envs:
        echo_failure('`{}` is not an available environment.'.format(env))
        echo_info('See what is available via `ddev start --list {}`.'.format(check))
        abort()

    echo_waiting('Setting up environment `{}`...'.format(env))
    config, metadata, error = start_environment(check, env)
    if error:
        echo_failure('Set up failed!')
        echo_waiting('Attempting to stop the environment...')
        stop_environment(check, env)
        abort(error)

    interface = get_interface(metadata)
    if interface is None:
        echo_failure('`{}` is an unsupported environment type.'.format(metadata['env_type']))
        echo_waiting('Attempting to stop the environment...')
        stop_environment(check, env)
        abort()

    environment = interface(check, env, config, metadata)

    echo_waiting('Writing the `{}` configuration for `{}`...'.format(check, env))
    environment.write_config()

    print(environment.locate_config())
    print(config)
    print(metadata)














