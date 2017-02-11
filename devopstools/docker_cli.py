import devopstools.general
import os
import argparse
import sys
import logging
import logging.config

import docker
from docker.client import Client
from docker.utils import kwargs_from_env
import dockerpty
import yaml

def create_parser(parent_parser, subparsers):

    docker_parser = subparsers.add_parser("docker", help="Docker commands",
                                          parents=[parent_parser])
    docker_parser.add_argument('-t', dest='image_tag', action='store', help="Image tag")
    docker_parser.add_argument('-p', dest='project_name', action='store', help="Project name")
    docker_parser.add_argument('-s', dest='service_name', action='store', help="Service name")
    docker_parser.set_defaults(func=main)

    action_subparser = docker_parser.add_subparsers(dest="action_command")

    action_subparser.add_parser("build", help="Docker-compose build", parents=[parent_parser])
    action_subparser.add_parser("config", help="Docker-compose config", parents=[parent_parser])
    action_subparser.add_parser("down", help="Docker-compose down", parents=[parent_parser])
    action_subparser.add_parser("execbash", help="Docker-compose exec bash", parents=[parent_parser])
    action_subparser.add_parser("logs", help="Docker-compose logs", parents=[parent_parser])
    action_subparser.add_parser("ps", help="Docker-compose ps", parents=[parent_parser])
    action_subparser.add_parser("psq", help="Docker-compose ps -q", parents=[parent_parser])

    runbash_parser = action_subparser.add_parser("runbash", help="Docker-compose run bash", parents=[parent_parser])
    runbash_parser.add_argument('-e', dest='entrypoint', action='store', help="Entrypoint", default="bash")

    action_subparser.add_parser("stop", help="Docker-compose stop", parents=[parent_parser])
    action_subparser.add_parser("upd", help="Docker-compose up -d", parents=[parent_parser])

    run_parser = action_subparser.add_parser("run", help="Docker-compose combine commands ",
                                             parents=[parent_parser])
    run_parser.add_argument('-b', dest='build', action='store_true', help="build")
    run_parser.add_argument('-u', '--upd', dest='upd', action='store_true', help="upd")
    run_parser.add_argument('-l', dest='logs', action='store_true', help="logs")

def main(args):
    DockerCli().main(args)

class DockerCli(object):
    """Docker CLI"""

    _scripts_path = None
    _logger = None
    _image_tag = None
    _project_name = None
    _service_name = None

    def __init__(self):
        self._scripts_path = os.path.dirname(os.path.abspath(__file__))

        self._docker_compose_path = os.environ.get("DEVOPSTOOLS_DOCKER_COMPOSE_PATH",
                                                   "./docker-compose/docker-compose.yml")

        logging.config.fileConfig(os.path.join(self._scripts_path, 'logging.conf'))
        self._logger = logging.getLogger('root')

    def main(self, args):
        self._logger.debug('Func: %s; args: %s', main.__name__, args)

        if not os.path.exists(self._docker_compose_path):
            print("Unable to read docker-compose at path (%s). "
                  "Override with env variable DEVOPSTOOLS_DOCKER_COMPOSE_PATH" %
                  self._docker_compose_path)
            sys.exit(1)

        self.set_image_name(args)
        self._project_name = args.project_name or self.get_project_name()
        self._service_name = args.service_name or "main"

        if args.action_command == "run":
            # NOTE: specific order required for piggyback
            if args.build:
                self.build(args)
            if args.upd:
                self.upd(args)
            if args.logs:
                self.logs(args)

        else:
            method_to_call = getattr(self, args.action_command)
            method_to_call(args)

    def generate_image_tag(self):
        """Generate image tag name from current .git branch """
        commands = [self._scripts_path + "/git-helper/git_helper_docker.sh",
                    self._scripts_path,
                    "get_git_docker_tag",
                    "main",
                    ""]
        image_tag = devopstools.general.exec_command(commands)

        return image_tag.replace("\n", "")

    def set_image_name(self, args):
        self._image_tag = args.image_tag or self.generate_image_tag()
        os.environ["image_tag"] = self._image_tag

        self._logger.info("image_tag = %s", os.environ.get("image_tag"))

    def load_docker_compose_yaml(self, filepath):
        docker_compose_yaml = None
        with open(filepath) as f:
            docker_compose_yaml = yaml.safe_load(f)

        return docker_compose_yaml

    def get_docker_compose_yaml_image(self):
        docker_compose_yaml = self.load_docker_compose_yaml(self._docker_compose_path)
        image = docker_compose_yaml["services"][self._service_name]["image"]

        return image.rsplit(':', 1)[0]

    def docker_compose_base(self):
        commands = ["docker-compose",
                    "-p",
                    self._project_name,
                    "-f",
                    self._docker_compose_path]
        return commands

    def exec_docker_compose(self, commands, realtime_output=False):
        final_commands = self.docker_compose_base() + commands
        self._logger.info(' '.join(final_commands))
        return devopstools.general.exec_command(final_commands, realtime_output)

    def build(self, args):
        commands = ["build", "--force-rm", self._service_name]
        print self.exec_docker_compose(commands)

    def config(self, args):
        commands = ["config"]
        print self.exec_docker_compose(commands)

    def execbash(self, args):
        ps_commands = ["ps", "-q", self._service_name]

        container_id = devopstools.general.exec_command(self.docker_compose_base() + ps_commands)
        container_id = container_id.replace("\n", "")

        self._logger.info("container_id = %s", container_id)

        cli = Client(version='auto', **kwargs_from_env())
        dockerpty.exec_command(cli, container_id, command='/bin/bash', interactive=True)

    def down(self, args):
        commands = ["down"]
        print self.exec_docker_compose(commands)

    def logs(self, args):
        commands = ["logs", self._service_name]
        print self.exec_docker_compose(commands, realtime_output=True)

    def ps(self, args):
        commands = ["ps", self._service_name]
        print self.exec_docker_compose(commands)

    def psq(self, args):
        commands = ["ps", "-q", self._service_name]
        print self.exec_docker_compose(commands)

    def runbash(self, args):
        image = "%s:%s" % (self.get_docker_compose_yaml_image(), self._image_tag)
        cli = Client(version='auto', **kwargs_from_env())
        container = cli.create_container(
            image=image,
            stdin_open=True,
            tty=True,
            entrypoint=args.entrypoint,
        )
        print("container started: ", container)
        dockerpty.start(cli, container)
        cli.remove_container(container)

    def stop(self, args):
        commands = ["stop", self._service_name]
        print self.exec_docker_compose(commands)

    def upd(self, args):
        commands = ["up", "-d", self._service_name]
        print self.exec_docker_compose(commands)

    def get_project_name(self):
        (head, tail) = os.path.split(os.getcwd())
        return tail

    def arguments(self):
        """Returns tuple containing dictionary of calling function's
            named arguments and a list of calling function's unnamed
            positional arguments.
        """
        try:
            from inspect import getargvalues, stack
            posname, kwname, args = getargvalues(stack()[1][0])[-3:]
            posargs = args.pop(posname, [])
            args.update(args.pop(kwname, []))
            return args, posargs
        except:
            raise
