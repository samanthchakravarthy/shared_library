#!/bin/bash
set -e

set reponame = $1
set jenkinsUrl = $2
set credential_Id = $3


CRUMB=$(curl -s 'http://example.com/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)' -u "admin":"11fc632b09259098c02a1f1bfc5b794040")
echo $CRUMB