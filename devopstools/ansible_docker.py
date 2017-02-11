import argparse
import logging
import os
import shutil
import stat
import subprocess
import sys

def create_parser(parent_parser, subparsers):
    """
    Create parser
    See https://docs.python.org/2/library/argparse.html#module-argparse
    """

    ansible_parser = subparsers.add_parser("ansible", help="Use container with Ansible",
                                           parents=[parent_parser])
    ansible_parser.set_defaults(func=main)

    action_subparser = ansible_parser.add_subparsers(dest="action_command")
    bash_parser = action_subparser.add_parser("bash", help="Bash",parents=[parent_parser])

    command_parser = action_subparser.add_parser("command", help="Command",parents=[parent_parser])
    command_parser.add_argument('cmd', action='store', help="Command to run")

    return ansible_parser

def main(args):
    AnsibleDocker().main(args)

class AnsibleDocker:

    def main(self, args):
        print "ansible_hello"
        print args

        dir_path = os.getcwd()
        print dir_path

        if args.action_command == "bash":
            print "docker-compose -f $(da_compose_file) run --rm main bash"

        if args.action_command == "command":
            print "docker-compose -f $(da_compose_file) run --rm main bash -c %s" \
                % args.cmd
