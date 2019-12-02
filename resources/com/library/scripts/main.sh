#!/bin/bash
set -e

set username = $1
set userid = $2
set password = $3
set reponame = $4
set repocreation = $5
set jenkinsUrl = $6
set credential_Id = $7
set CIJenkinsjobCreation = $8
set technology = $9


if [ "$repocreation" = true ] ; then
set +x      # turn off echo
bash resources/com/library/scripts/bitbucket.sh $username $userid $password $reponame $technology
set -x      # turn on echo
echo "Creation of repo completed"
sleep 10
fi

if [ "$CIJenkinsjobCreation" = true ] ; then
set +x      # turn off echo
bash resources/com/library/scripts/cijob.sh $reponame $jenkinsUrl $credential_Id
set -x      # turn on echo
echo "CI multibranch pipeline job created successfully"
sleep 10
fi