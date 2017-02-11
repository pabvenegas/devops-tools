#!/bin/bash

# set -x


# Get Branch name, if not a git repository then use $USER
function git_docker_branch_name()
{
  source ${devops_tools_path}/git-helper/git_helper.sh

  local branch_name

  if [ ! -d ".git" ]; then
    branch_name=$USER
  else
    branch_name=$(get_git_branch_name)
  fi
  echo "${branch_name}"
}

# Sanitise branch name to be valid docker image tag 
function get_sanitise_branch_name_for_docker_tag()
{
  branch_name_value=$(git_docker_branch_name) 
  # replace / with -
  sanitised_branch_name=`echo ${branch_name_value} | cut -d'-' -f 1,2 | sed -e 's/\//-/g'`
  echo "${sanitised_branch_name}"
}

# If git branch is NOT master then
# prefix docker image tag name with git branch name
function get_git_docker_tag()
{
  source ${devops_tools_path}/git-helper/git_helper.sh

  local docker_tag
  sanitised_branch_name=$(get_sanitise_branch_name_for_docker_tag)
  git_commit=$(get_git_commit)

  image_tag_prefix_value=$(get_docker_image_tag_prefix)

  if [ "${sanitised_branch_name}" == "master" ]; then
    docker_tag="${image_tag_prefix_value}${git_commit}"
  else
    docker_tag="${sanitised_branch_name}-${image_tag_prefix_value}${git_commit}"
  fi

  if [ ! -z "${tag_suffix}" ]; then
    docker_tag="${docker_tag}-${tag_suffix}"
  fi

  echo "${docker_tag}"
}

# if container repository has defined IMAGE_TAG_PREFIX get value
# by referencing 'load_env.sh'
function get_docker_image_tag_prefix()
{
  source docker-compose/load_env.sh "${service_name}"

  local image_tag_prefix_value
  if [ ! -z "${IMAGE_TAG_PREFIX}" ]; then
    image_tag_prefix_value="${IMAGE_TAG_PREFIX}-"
  fi
  echo "${image_tag_prefix_value}"
}

devops_tools_path=$1
run_function=$2
service_name=$3
tag_suffix=$4

echo "$(${run_function})"