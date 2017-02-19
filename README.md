# DEVOPS TOOLS #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Usage ###

```
# show commands
devops_tools -h
devops_tools docker -h

# generate docker code from template
devops_tools docker generate
devops_tools docker generate --imagename dtr.com/pabvenegas/gentest

# docker build upd logs
docker_tools docker run -b -u -l

# start container use entrypoint bash
docker_tools docker runbash

# exec to existing container
docker_tools docker execbash
```

### How do I get set up? ###

* Summary of set up

```
virtualenv venv

source venv/bin/activate
python setup.py build
python setup.py install
devops_tools -h
deactivate

```

* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

```
## Local Dev

# cd to repo parent folder
sudo -H pip install [repo_path]/devops_tools/
sudo -H pip uninstall -y devops_tools

## Upload to pypi
pip install twine

python setup.py sdist bdist_wheel
twine upload dist/*

## pip install (from pypi.org)

pip install -vvv devops-tools
pip uninstall -y devops-tools

```

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact