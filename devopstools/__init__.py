'''
devopstools: Main module

Copyright 2017, PV
Licensed under MIT.
'''
import argparse
import logging
import logging.config
import sys
import os
import shutil
import yaml

import devopstools.docker_cli
import devopstools.ansible_docker
import devopstools.general

def create_parser():
    """
    Create parser
    See https://docs.python.org/2/library/argparse.html#module-argparse
    """
    parent_parser = argparse.ArgumentParser(add_help=False)

    main_parser = argparse.ArgumentParser()
    service_subparsers = main_parser.add_subparsers(dest="service_command")

    config_parser = service_subparsers.add_parser("config", help="Config helper commands",parents=[parent_parser])
    config_parser.set_defaults(func=config_help)
    action_subparser = config_parser.add_subparsers(dest="action_command")
    action_subparser.add_parser("create", help="Create local config file", parents=[parent_parser])

    devopstools.docker_cli.create_parser(parent_parser, service_subparsers)
    devopstools.ansible_docker.create_parser(parent_parser, service_subparsers)

    return main_parser

def config_help(args, logger, config):
    """ Config help parser """

    if args.action_command == "create":
        DevopsToolsConfig(logger).create_local_config_file()

def main():
    parser = create_parser()
    args = parser.parse_args()

    scripts_path = os.path.dirname(os.path.abspath(__file__))

    logging.config.fileConfig(os.path.join(scripts_path, 'logging.conf'))
    logger = logging.getLogger('root')

    config_file = DevopsToolsConfig(logger).load_config_file()
    with open(config_file) as f:
        config = yaml.safe_load(f)

    args.func(args, logger, config)

class DevopsToolsConfig(object):

    def __init__(self, logger):
        self._scripts_path = os.path.dirname(os.path.abspath(__file__))
        self._logger = logger

        self._default_config_env_var = "DEVOPSTOOLS_CFG"
        self._default_config_file_name = "devopstools.cfg"
        self._default_config_file_path = os.path.join(self._scripts_path,
                                                      self._default_config_file_name)

    def load_config_file(self):
        """ Load config file for system, attempt to load in following order:
        1) env var DEVOPSTOOLS_CFG
        2) current path file 'devopstools.cfg'
        3) installation config file
        """
        config_file = None

        env_var_config_file = os.getenv(self._default_config_env_var)
        if env_var_config_file:
            config_file = env_var_config_file
            if not os.path.exists(config_file):
                self._logger.debug("Config file path from %s (%s) not found",
                             self._default_config_env_var, env_var_config_file)
                config_file = None

        if not config_file:
            config_file = os.path.join(os.getcwd(), self._default_config_file_name)
            if not os.path.exists(config_file):
                self._logger.debug("Config file at current path not found, defaulting to installation config file")
                config_file = None

        if not config_file:
            config_file = self._default_config_file_path

        return config_file

    def create_local_config_file(self):
        """ Create local copy of config file """
        local_config_path = os.path.join(os.getcwd(), self._default_config_file_name)
        shutil.copyfile(self._default_config_file_path, local_config_path)
        print "Local config file created %s" % local_config_path
