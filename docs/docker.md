## Docker Development Environment

Docker can be used to created a local dev environment. This offers two main advantages:

- You don't have to worry about installing the right version of python and any other dependencies
- The requirments for a local development evnironment are clearly documented and tested

The following command will prepare a docker container for you, and make the repo avaialble to you.
```
cd docker-dev && \
docker build -t devopstools-dev-image . && \
cd ../ && \
docker run -it --rm --name devopstools-dev-container \
-v "$PWD":/usr/src/dev \
-w /usr/src/dev \
devopstools-dev-image bash
```