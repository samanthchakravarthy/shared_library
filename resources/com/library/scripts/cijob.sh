#!/bin/bash
set -e

set reponame = $1
set jenkinsUrl = $2
set credential_Id = $3

username="admin"
API_TOKEN="11fc632b09259098c02a1f1bfc5b794040"

echo "hello"

CRUMB=$(curl -s '$jenkinsUrl/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)' -u $username:$API_TOKEN)
echo $CRUMB

curl -X GET '$jenkinsUrl/job/java-pipeline/config.xml' -u $username:$API_TOKEN -o mylocalconfig.xml

ls -ltR
cat ylocalconfig.xml