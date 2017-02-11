# Test Container

## Local build

### Local docker-compose

```
# replace "manual" as you please
export image_tag=manual; docker-compose -f docker-compose/docker-compose.yml up -d
export image_tag=manual; docker-compose -f docker-compose/docker-compose.yml down

```

### Local devops_tools build

```
# run unset if you have used manual command above i.e export image_tag=manual;
unset image_tag

devops_tools docker build
devops_tools docker up
devops_tools docker logs

# build upd logs in one command
devops_tools docker run -b -u -l

```
