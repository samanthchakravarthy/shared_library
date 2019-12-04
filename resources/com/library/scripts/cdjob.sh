#!/bin/bash
set -e

set reponame = $1
set jenkinsUrl = $2
set credential_Id = $3
set CDJenkinsjobCreation = $4


username="admin"
API_TOKEN="11fc632b09259098c02a1f1bfc5b794040"

echo "hello"

CRUMB=$(curl -s ''$jenkinsUrl'/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)' -u "$username":"$API_TOKEN")
echo $CRUMB

curl -X GET "$jenkinsUrl/job/java-deployment-pipeline/config.xml" -u "$username":"$API_TOKEN" -o localconfig.xml

curl -X POST "$jenkinsUrl/createItem?name=deploy&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json={"name":"FolderName","mode":"com.cloudbees.hudson.plugins.folder.Folder","from":"","Submit":"OK"}&Submit=OK" -u "$username":"$API_TOKEN" -H "$CRUMB" -H "Content-Type:application/x-www-form-urlencoded"
echo "deploy folder created successfully"

for job in DEV QA PROD
do 
  echo "inside for"
  if [[ $job == 'DEV' ]]; then
      echo $job
      curl -X POST "$jenkinsUrl/job/deploy/createItem?name=DEV&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json={"name":"FolderName","mode":"com.cloudbees.hudson.plugins.folder.Folder","from":"","Submit":"OK"}&Submit=OK" -u "$username":"$API_TOKEN" -H "$CRUMB" -H "Content-Type:application/x-www-form-urlencoded"
      echo "dev folder created"
  elif [[ $job == 'QA' ]]; then
      echo $job
      curl -X POST "$jenkinsUrl/job/deploy/createItem?name=QA&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json={"name":"FolderName","mode":"com.cloudbees.hudson.plugins.folder.Folder","from":"","Submit":"OK"}&Submit=OK" -u "$username":"$API_TOKEN" -H "$CRUMB" -H "Content-Type:application/x-www-form-urlencoded"
      echo "qa folder created"
  elif [[ $job == 'PROD' ]]; then
      echo $job
      curl -X POST "$jenkinsUrl/job/deploy/createItem?name=PROD&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json={"name":"FolderName","mode":"com.cloudbees.hudson.plugins.folder.Folder","from":"","Submit":"OK"}&Submit=OK" -u "$username":"$API_TOKEN" -H "$CRUMB" -H "Content-Type:application/x-www-form-urlencoded"
      echo "prod folder created"
   else
      echo "Skip CD job creation"
   fi  
done   

cat localconfig.xml 

curl -X POST "$jenkinsUrl/job/deploy/job/$job/createItem?name=$reponame" -u "$username":"$API_TOKEN" --data "@localconfig.xml" -H "$CRUMB" -H "Content-Type:application/x-www-form-urlencoded"

echo "created cd job"
