#!/bin/bash
set -e

set username = $1
set user = $2
set password = $3
set reponame = $4
set scm_repocreation = $5


if [ "$repocreation" = true ] ; then
set +x      # turn off echo
sh resources/com/library/scripts/bitbucket.sh $username $user $password $reponame
set -x      # turn on echo
echo "Creation of repo completed"
sleep 10
fi