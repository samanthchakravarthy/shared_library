#!/bin/bash
set -e

set username = $1
set userid = $2
set password = $3
set reponame = $4
set repocreation = $5


if [ "$repocreation" = true ] ; then
set +x      # turn off echo
bash resources/com/library/scripts/bitbucket.sh $username $userid $password $reponame
set -x      # turn on echo
echo "Creation of repo completed"
sleep 10
fi