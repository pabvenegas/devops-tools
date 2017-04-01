*** :: warning :: this repo is still in beta mode ***

DevOps Tools is a python package that provides a number of handy helper functions for developers.

You can get the latest version of [devops-tools](https://pypi.python.org/pypi/devops-tools/) as a python package on [PyPI](https://pypi.python.org/pypi).

If you already have python & pip, try: `pip install devops-tools`.

# Usage

DevOps Tools is operated via arguments passed to the python script.

** Show available commands **

You can use the `-h` flag to explore the available commands e.g `devops_tools -h`.

```
usage: devops_tools [-h] {docker,ansible,generate} ...

positional arguments:
  {docker,ansible,generate}
    docker              Docker commands
    ansible             Use container with Ansible
    generate            Use template to generate docker container

optional arguments:
  -h, --help            show this help message and exit
```

** Positional Arguments **

Positional arguments are special arguments that are passed to the DevOps Tools script.

There are three positional arguments to choose from: `docker`, `ansible` and `generate`.

Each positional argument has it's own help seciton too, e.g `devops_tools docker -h`.

# Commands

Each positional argument is an available command: `docker`, `ansible` and `generate`.

You can [learn more about what commands are available](docs/commands.md).

# Installation

You can get the latest version of [devops-tools](https://pypi.python.org/pypi/devops-tools/) as a python package on [PyPI](https://pypi.python.org/pypi).

If you already have python & pip, try: `pip install devops-tools`.

You can uninstall with `pip uninstall devops-tools`

# Contributing

You can contirbute to this project like any other python project.

If you have Docker installed, you may want to develop and test with an [isolated docker container](docs/docker.md). You can also develop on your local workstation if you prefer.

** Build/Install from source (this repo) **

Using this repo, you can build/install `devops_tools`. You'll need a valid development environment (we recommend python and virtaulenv).

```
virtualenv venv
source venv/bin/activate
python setup.py build
python setup.py install
```

You should now be able to run `devops_tools -h`.

When done, you should run `deactivate`.

** Installing/Uninstalling **

```
pip install ./
pip uninstall -y devops_tools
```

** Upload to PyPI **

You can upload to [PyPI](https://pypi.python.org/pypi)
```
## Upload to pypi
pip install twine

python setup.py sdist bdist_wheel
twine upload dist/*
```
