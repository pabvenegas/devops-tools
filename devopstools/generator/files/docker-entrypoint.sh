#!/bin/bash

# set -x

echo -e "\n"
echo '-----------------'
echo "devops-generator: Successfully loaded container $HOSTNAME"
echo ""
echo "** REMOVE THIS SECTION (only for docker-generator) **"
echo '-----------------'

if [ "$1" == "main" ]; then
  echo "Main parameter parsed"
else
  exec "$@"
fi