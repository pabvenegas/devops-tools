import os

import devopstools.general
from getpass import getpass, _raw_input

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
    dir_path = os.getcwd()

    if args.action_command == "create":
        # msg =
        print("This will overwrite files at: %s" % dir_path)
        create_continue = _raw_input("Do you wish to continue? (y/n)")

        if create_continue == "y":
            commands = ["mkdir", "tmp"]
            print commands
            devopstools.general.exec_command(commands)

            from_path = file_path + "/" + "generator/"
            to_path = "./tmp"
            commands = ["cp", "-r", from_path, to_path]
            print commands
            devopstools.general.exec_command(commands)
