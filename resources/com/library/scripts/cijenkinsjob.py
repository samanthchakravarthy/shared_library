'''
this script creates a jenkins job from an xml file
'''

import jenkins
import os,sys
import xml.etree.ElementTree as ET
import requests

userName = "admin"
password = "admin"
jenkins_job_name = sys.argv[1]
jenkinsUrl = sys.argv[2]
credential_Id = sys.argv[3]

try:
    jenkins_obj = jenkins.Jenkins(jenkinsUrl, userName, password)
except:
    print("Invalid Credentials or Jenkins url")

os.system('ls -ltR')

tree = ET.parse('template/multibranch.xml')
root = tree.getroot()
config_file = ET.tostring(root, encoding='utf8', method='xml').decode()
config_file = config_file.replace('{credential_Id}', credential_Id)
config_file = config_file.replace('{jenkins_job_name}', jenkins_job_name)
print(jenkins_obj.create_job(jenkins_job_name, config_file)) # create Jenkins jobs