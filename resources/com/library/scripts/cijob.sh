#!/bin/bash
set -e

set reponame = $1
set jenkinsUrl = $2
set credential_Id = $3

username="admin"
API_TOKEN="11fc632b09259098c02a1f1bfc5b794040"

echo "hello"


#CRUMB=$(curl -s -u "$username":"$API_TOKEN" "$jenkinsUrl/crumbIssuer/api/json")

CRUMB=$(curl -s ''$jenkinsUrl'/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)' -u "$username":"$API_TOKEN")


echo $CRUMB

curl -X GET "$jenkinsUrl/job/java-pipeline/config.xml" -u "$username":"$API_TOKEN" -o mylocalconfig.xml

#ls -ltR
#cat mylocalconfig.xml

echo "reading a file"


while read a; do
    echo ${a//"snowball.git"/"$reponame.git"}
done < mylocalconfig.xml > localconfig.xml
#mv mylocalconfig.xml{.t,}

cat mylocalconfig.xml

curl -X POST "$jenkinsUrl/createItem?name=$reponame" -u "$username":"$API_TOKEN" --data "@localconfig.xml" -H "$CRUMB" -H "Content-Type:application/xml"


#curl -X POST -H "$CRUMB" -H "content-type:application/xml" --data "@/resources/com/library/scripts/template/multibranch.xml" "$jenkinsUrl/createItem?name=""" --trace-ascii /dev/stdout 