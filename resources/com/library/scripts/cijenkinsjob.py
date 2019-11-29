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




def build_jenkins_job(url, username, password):
    """Post to the specified Jenkins URL.

    `username` is a valid user, and `password` is the user's password or
    (preferably) hex API token.
    """
    # Build the Jenkins crumb issuer URL
    parsed_url = urllib.parse.urlparse(url)
    crumb_issuer_url = urllib.parse.urlunparse((parsed_url.scheme,
                                                parsed_url.netloc,
                                                'crumbIssuer/api/json',
                                                '', '', ''))

    # Get the Jenkins crumb
    auth = requests.auth.HTTPBasicAuth(username, password)
    r = requests.get(crumb_issuer_url, auth=auth)
    json = r.json()
    crumb = {json['crumbRequestField']: json['crumb']}
    print("['crumb']" , crumb)
    # POST to the specified URL
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    headers.update(crumb)
    r = requests.post(url, headers=headers, auth=auth)

username = 'jenkins'
password = '3905697dd052ad99661d9e9f01d4c045'
url = jenkinsUrl 
build_jenkins_job(url, username, password)

try:
    jenkins_obj = jenkins.Jenkins(jenkinsUrl, userName, password)
except:
    print("Invalid Credentials or Jenkins url")


tree = ET.parse('resources/com/library/scripts/template/multibranch.xml')
root = tree.getroot()
config_file = ET.tostring(root, encoding='utf8', method='xml').decode()
config_file = config_file.replace('{credential_Id}', credential_Id)
config_file = config_file.replace('{jenkins_job_name}', jenkins_job_name)
print(jenkins_obj.create_job(jenkins_job_name, config_file)) # create Jenkins jobs