#!/bin/bash
set -e

set reponame = $1
set jenkinsUrl = $2
set credential_Id = $3

username="admin"
API_TOKEN="11fc632b09259098c02a1f1bfc5b794040"

echo "hello"

if test -e mylocalconfig.xml; then
	rm mylocalconfig.xml
fi

if test -e localconfig.xml; then
	rm localconfig.xml
fi

CRUMB=$(curl -s ''$jenkinsUrl'/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)' -u "$username":"$API_TOKEN")
echo $CRUMB

curl -X GET "$jenkinsUrl/job/dataquality/config.xml" -u "$username":"$API_TOKEN" -o mylocalconfig.xml


while read a; do
    echo ${a//"test-demo.git"/"$reponame.git"}
done < mylocalconfig.xml > localconfig.xml
echo "</org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject>" >> localconfig.xml

#cat localconfig.xml

curl -X POST "$jenkinsUrl/createItem?name=$reponame" -u "$username":"$API_TOKEN" --data "@localconfig.xml" -H "$CRUMB" -H "Content-Type:application/xml"

 