import jenkins
import sys
import xml.etree.ElementTree as ET
import requests

def main(**kwargs):
 reponame=kwargs['reponame']
 jenkinsUrl=kwargs['jenkinsUrl']
 credential_Id=kwargs['credential_Id']
 CDJenkinsjobCreation=kwargs['CDJenkinsjobCreation']
 username = "admin"
 API_TOKEN = "11fc632b09259098c02a1f1bfc5b794040"

 cdJob=CDJenkinsjobCreation.split(',')

 jenkins_url = jenkinsUrl + "/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,%22:%22,//crumb)"
 crumb_response = requests.get(url=jenkins_url, auth=(username, API_TOKEN))
 crumb_id = crumb_response.text.split(':')[1]
 headers = {"Content-Type": "application/x-www-form-urlencoded", "Jenkins-Crumb": crumb_id}
 jenkins_url = jenkinsUrl + "createItem?name=deploy&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json=%7B%22name%22%3A%22FolderName%22%2C%22mode%22%3A%22com.cloudbees.hudson.plugins.folder.Folder%22%2C%22from%22%3A%22%22%2C%22Submit%22%3A%22OK%22%7D&Submit=OK"
 response = requests.post(url=jenkins_url, auth=(username, API_TOKEN), headers=headers)
 print(response)

 jenkins_obj = jenkins.Jenkins(jenkinsUrl, username, API_TOKEN)
 # template used to create pipeline job
 tree = ET.parse('resources/com/library/scripts/template/deploy_pipelineJob.xml')
 root = tree.getroot()
 config_file = ET.tostring(root, encoding='utf8', method='xml').decode()

 for job in cdJob:
     if(job=='DEV'):
      jenkins_url = jenkinsUrl + "job/deploy/createItem?name=" + job + "&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json=%7B%22name%22%3A%22FolderName%22%2C%22mode%22%3A%22com.cloudbees.hudson.plugins.folder.Folder%22%2C%22from%22%3A%22%22%2C%22Submit%22%3A%22OK%22%7D&Submit=OK"
      response = requests.post(url=jenkins_url, auth=(username, API_TOKEN), headers=headers)
      print(response)
      jenkins_url = jenkins_obj.create_job("deploy/" + job + "/" + reponame, config_file)
     elif(job=='QA'):
      jenkins_url = jenkinsUrl + "job/deploy/createItem?name=" + job + "&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json=%7B%22name%22%3A%22FolderName%22%2C%22mode%22%3A%22com.cloudbees.hudson.plugins.folder.Folder%22%2C%22from%22%3A%22%22%2C%22Submit%22%3A%22OK%22%7D&Submit=OK"
      response = requests.post(url=jenkins_url, auth=(username, API_TOKEN), headers=headers)
      print(response)
      jenkins_url = jenkins_obj.create_job("deploy/" + job + "/" + reponame, config_file)
     elif(job=='PROD'):
      jenkins_url = jenkinsUrl + "job/deploy/createItem?name=" + job + "&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json=%7B%22name%22%3A%22FolderName%22%2C%22mode%22%3A%22com.cloudbees.hudson.plugins.folder.Folder%22%2C%22from%22%3A%22%22%2C%22Submit%22%3A%22OK%22%7D&Submit=OK"
      response = requests.post(url=jenkins_url, auth=(username, API_TOKEN), headers=headers)
      print(response)
      jenkins_url = jenkins_obj.create_job("deploy/" + job + "/" + reponame, config_file)
     else:
      print('Skip creating CD JOB')

if __name__ == '__main__':
    # prepare the input args for the main function and call the main func
    params = dict(arg.split('=') for arg in sys.argv[1:])
    main(**params)