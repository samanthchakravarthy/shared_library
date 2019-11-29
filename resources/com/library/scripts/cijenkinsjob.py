'''
this script creates a jenkins job from an xml file
'''

import jenkins
import os,sys
import xml.etree.ElementTree as ET
import requests
import urllib.parse


userName = "admin"
#11fc632b09259098c02a1f1bfc5b794040
password = "11fc632b09259098c02a1f1bfc5b794040"
jenkins_job_name = sys.argv[1]
jenkinsUrl = sys.argv[2]
credential_Id = sys.argv[3]


# api to generate crumb_id
jenkins_url = jenkinsUrl +"/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,%22:%22,//crumb)"
crumb_response = requests.get(url = jenkins_url, auth=(userName, password))
crumb_id = crumb_response.text.split(':')[1]

print("crumb_id :",crumb_id)
jenkins_url = jenkinsUrl+"/job/JOB_NAME/build"

tree = ET.parse('resources/com/library/scripts/template/multibranch.xml')
root = tree.getroot()
config_file = ET.tostring(root, encoding='utf8', method='xml').decode()
config_file = config_file.replace('{credential_Id}', credential_Id)
config_file = config_file.replace('{jenkins_job_name}', jenkins_job_name)

myfile = open("mbpj.xml", "w")
myfile.write(myfile)

os.system("ls -ltR")
headers = {"Content-Type": "application/x-www-form-urlencoded", "Jenkins-Crumb": crumb_id}
payload = ( ('file0', open("mbpj.xml", "rb")),
            ('json', '{ "parameter": [ {"name":"mbpj.xml", "file":"file0" }]}' ))


#try:
#    jenkins_obj = jenkins.Jenkins(jenkinsUrl, userName, password)
#except:
#    print("Invalid Credentials or Jenkins url")




resp = requests.post(jenkins_url, auth=('username','password'), headers=headers, files=payload)

#print(jenkins_obj.create_job(jenkins_job_name, config_file)) # create Jenkins jobs