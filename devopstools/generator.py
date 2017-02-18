import os
from getpass import getpass, _raw_input
import logging
import logging.config
import sys
import yaml

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

    action_subparser = generator_parser.add_subparsers(dest="action_command")

    generate_parser = action_subparser.add_parser("generate", help="Generate new docker container",
                                                  parents=[parent_parser])
    generate_parser.add_argument('-i', "--imagename", dest='image_name', action='store',
                                 help="Image Name for docker container")

    return generator_parser


def main(args):
    Generator().main(args)

class Generator(object):
    """Generator"""

    def __init__(self):
        self._scripts_path = os.path.dirname(os.path.abspath(__file__))
        logging.config.fileConfig(os.path.join(self._scripts_path, 'logging.conf'))
        self._logger = logging.getLogger('root')

        self._cwd = os.getcwd()
        self._default_image_name = "registry/group/repo"
        self._default_dest_folder = "."

    def main(self, args):
        self._logger.debug('Func: %s; args: %s', main.__name__, args)

        if args.action_command == "run":
            print "dummy"
        else:
            method_to_call = getattr(self, args.action_command)
            method_to_call(args)

    def generate(self, args):
        """ Generate a docker container """

        dest_folder = raw_input("Please enter destination folder path ? [%s] " \
                                % self._default_dest_folder)
        if dest_folder.startswith('/'):
            print "Destination folder must be relative, cannot start with '/'"
            sys.exit(1)

        if not dest_folder:
            dest_folder = self._default_dest_folder

        dest_path = os.path.join(self._cwd, dest_folder.strip())
        print("This will copy files to: %s" % dest_path)
        create_continue = _raw_input("Do you wish to continue? (y/n) ")

        if create_continue == "y":
            from_path = os.path.join(self._scripts_path, "generator/")
            if not os.path.exists(from_path):
                print "Unable to find generate template path (%s)" % from_path
                sys.exit(1)

            commands = ["cp", "-r", from_path, dest_path]
            devopstools.general.exec_command(commands)

            image_name = args.image_name
            if not args.image_name:
                image_name = raw_input("Please enter image_name ? [%s] " % self._default_image_name)
                if not image_name:
                    image_name = self._default_image_name

            generated_docker_compose = os.path.join(dest_path, "docker-compose", "docker-compose.yml")

            loaded_yaml = devopstools.general.load_yaml_file(generated_docker_compose)
            loaded_yaml["services"]["main"]["image"] = "%s:${image_tag}" % image_name

            devopstools.general.write_yaml_file(loaded_yaml, generated_docker_compose)

