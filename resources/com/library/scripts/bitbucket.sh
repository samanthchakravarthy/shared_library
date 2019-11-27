#!/bin/bash
set -e
echo "heloo"

set username = $1
set user = $2
set password = $3
set reponame = $4

pass="$password"

if [[ "${pass}" =~ "@" ]] ;then
	replace="%40"
	p=$(echo ${pass/@/$replace})
	pass=$p
fi

if [[ "${user}" =~ "@" ]] ;then
	replace="%40"
	p=$(echo ${user/@/$replace})
	user=$p
fi

echo "Execute a curl command to create remote repository in the bitbucket"
    
curl -X POST -H "Content-Type: application/json" \
"https://"$user":"$pass"@api.bitbucket.org/2.0/repositories/"$username"/"$reponame"" \
-d '{"scm": "git"}'
        

git config --global user.email $user
git config --global user.name $username

echo "Clone the remote repository"



if git clone https://$username@bitbucket.org/$username/$reponame.git 2> /dev/null; then
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
	if git push origin master --quiet 2> /dev/null; then
		echo "pushed the sourcecode to master"
	fi

echo "create a develop branch locally"

	git checkout -b develop

echo "push develop branch to remote repository"
	
	if git push --set-upstream origin develop --quiet 2> /dev/null; then
	echo "pushed the sourcecode to develop"
	fi

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