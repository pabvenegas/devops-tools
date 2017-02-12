import os
from getpass import getpass, _raw_input
import sys

import devopstools.general


def create_parser(parent_parser, subparsers):
    """
    Create parser
    See https://docs.python.org/2/library/argparse.html#module-argparse
    """

    generator_parser = subparsers.add_parser("generate",
                                             help="Use template to generate docker container",
                                             parents=[parent_parser])
    generator_parser.set_defaults(func=main)

    action_subparser = generator_parser.add_subparsers(
        dest="action_command")

    create_parser = action_subparser.add_parser("create", help="Create new",
                                                parents=[parent_parser])
    update_parser = action_subparser.add_parser("update", help="Update existing",
                                                parents=[parent_parser])

    return generator_parser


def main(args):
    file_path = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()

    if args.action_command == "create":

        folder = raw_input("Please enter destination folder path ? [.] ")
        if folder.startswith('/'):
            print "Destination folder must be relative, cannot start with '/'"
            sys.exit(1)

        if not folder:
            folder = "."

        dest_path = os.path.join(cwd, folder.strip())
        print("This will copy files to: %s" % dest_path)
        create_continue = _raw_input("Do you wish to continue? (y/n) ")

        if create_continue == "y":
            from_path = os.path.join(file_path, "generator/")
            if not os.path.exists(from_path):
                print "Unable to find generate template path (%s)" % from_path
                sys.exit(1)

            commands = ["cp", "-r", from_path, dest_path]
            # print commands
            devopstools.general.exec_command(commands)

