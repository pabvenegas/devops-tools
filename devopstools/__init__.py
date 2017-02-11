'''
devopstools: Main module

Copyright 2017, PV
Licensed under MIT.
'''
import argparse
import sys

import devopstools.docker_cli
import devopstools.ansible_docker
import devopstools.generator

def create_parser():
    """
    Create parser
    See https://docs.python.org/2/library/argparse.html#module-argparse
    """
    parent_parser = argparse.ArgumentParser(add_help=False)

    main_parser = argparse.ArgumentParser()
    service_subparsers = main_parser.add_subparsers(
        dest="service_command")

    devopstools.docker_cli.create_parser(parent_parser, service_subparsers)
    devopstools.ansible_docker.create_parser(parent_parser, service_subparsers)
    devopstools.generator.create_parser(parent_parser, service_subparsers)

    return main_parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    args.func(args)
