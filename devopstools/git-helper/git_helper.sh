#!/bin/bash

# set -x

function get_git_branch_name
{
  local branch_name

  branch_name=$(git symbolic-ref -q HEAD)
  branch_name=${branch_name##refs/heads/}
  branch_name=${branch_name:-HEAD}

  echo "${branch_name}"
}

# http://softwareengineering.stackexchange.com/questions/141973/how-do-you-achieve-a-numeric-versioning-scheme-with-git
# Small improvement: git describe --long --tags --dirty --always. 
# 'Dirty' will tell you if there were local changes when the 'describe' was done (meaning it can't fully describe the state of the repo). 
# 'Always' means you won't get an error when there are no tags. 
# It will fallback to just a commit hash. 
# So you can get 76001f2-dirty as an example. 
# Obviously, seeing 'dirty' means somebody messed up

function get_git_commit()
{
  if [ -d ".git" ]; then
    branch_name=$(get_git_branch_name)

    if [ "$branch_name" == "master" ]; then
      GIT_COMMIT=`git describe --long 2>/dev/null`
    else
      GIT_COMMIT=`git describe --tags 2>/dev/null`
    fi

    if [ -z "$GIT_COMMIT" ]
    then
      # Give us a variable to show the latest tag + commits since last tag + SHA of HEAD
      # eg - v1.0.2-166-g65c5afb
      GIT_COMMIT=`git describe --long 2>/dev/null`
      if [ -z "$GIT_COMMIT" ]
      then
        GIT_COMMIT=`git describe --long --first-parent 2>/dev/null`
        # if there are NO tags for this repo, try just checking for branches
        if [ $? -ne 0 ]; then
          # Using GIT_COMMIT=`git describe --all --first-parent` results invalid tag 
          # so using 0 to pass for the moment, make obvious something is wrong
          GIT_COMMIT="0"
        fi
      fi
    fi
  else
    # "Folder does not appear to be a git repository - defaulting GIT SHA to 0"
    GIT_COMMIT="0"
  fi

  echo "${GIT_COMMIT}"
}

run_function=$1
if [ ! -z "${run_function}" ]; then
  echo "$(${run_function})"
fi