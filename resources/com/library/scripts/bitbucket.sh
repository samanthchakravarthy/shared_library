#!/bin/bash

set -e
echo "heloo"

set username = $1
set userid = $2
set password = $3
set reponame = $4

pass="$password"

pass=$(echo ${pass/@/"%40"})
pass=$(echo ${pass/\?/"%3F"})
pass=$(echo ${pass/\//"%2F"})

user="$userid"

user=$(echo ${user/@/"%40"})


echo "Execute a curl command to create remote repository in the bitbucket"
    
curl -X POST -H "Content-Type: application/json" \
"https://"$user":"$pass"@api.bitbucket.org/2.0/repositories/"$username"/"$reponame"" \
-d '{"scm": "git"}'
        

git config --global user.email $userid
git config --global user.name $username

echo "Clone the remote repository"



if git clone https://"$user":"$pass"@bitbucket.org/$username/$reponame.git 2> /dev/null; then
	echo "Clone the remote repository"
else
    echo "Invalid credentials or project key"
fi

cd $reponame

echo "Add files"
    
	touch readme.md
	touch .gitignore

echo "Add git add/commit/push changes to remote repository"

	git add --all
	git commit -m "Initial commit"
	git push origin master
	echo "pushed the sourcecode to master"
	

echo "create a develop branch locally"

	git checkout -b develop

echo "push develop branch to remote repository"
	
	git push --set-upstream origin develop
	echo "pushed the sourcecode to develop"


echo "Execute a curl command to set branch permissions"

declare -a modelbranchs=("develop" "master")
for mbranch in "${modelbranchs[@]}"
do
	declare -a restypes=("delete" "push")
	for rtype in "${restypes[@]}"
	do
		curl -X POST -H "Content-Type: application/json" \
		"https://"$user":"$pass"@api.bitbucket.org/2.0/repositories/"$username"/"$reponame"/branch-restrictions" \
		-d '{
			"kind" : "'$rtype'" ,
			"links" : {
				"self" : {
					"href" : "refs/heads/'$mbranch'",
					"name" : "'$mbranch'"
					}
				},
			"pattern": "'$mbranch'",
			"branch_match_kind": "glob"
		}'
	done
done

cd ..