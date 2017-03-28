#### Docker

The docker command has a number of functions to make day to day docker deveopment easy.

##### Generate docker code from template

`generate` will use template to generate docker container

```
devops_tools docker generate
devops_tools docker generate --imagename dtr.com/pabvenegas/gentest
```

##### Docker Run

Docker Run will run a container. With the right arguments you can `build` (from your pwd), `upd`, then show `logs`.

```
docker_tools docker run -b -u -l
```

##### Docker Run :: Bash

You can start container using bash as the entrypoint `docker_tools docker runbash`.

You can exec to existing container `docker_tools docker execbash`.