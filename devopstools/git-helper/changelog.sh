#!/bin/bash
# Author:Andrey Nikishaev
# Thanks to Andrey, we can now use this script to generate changelog which writes
# our commit subject to CHANGELOG.md. This is just a starting point and we might
# need to modify this if we want make it more verbose.


echo "# CHANGELOG"
git tag -l | sort -nr | while read TAG ; do
    echo
    if [ $NEXT ];then
        echo "## ${NEXT}"
    else
        echo "## Current"
    fi
    GIT_PAGER=cat git log --no-merges --format=" * %s" $TAG..$NEXT
    NEXT=$TAG
done
FIRST=$(git tag -l | sort -n | head -1)
echo
echo "## ${FIRST}"
GIT_PAGER=cat git log --no-merges --format=" * %s" $FIRST
