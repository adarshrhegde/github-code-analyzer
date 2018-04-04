# -*- coding: utf-8 -*-

import requests
import subprocess
import logging
import os

#get all java repo
repo = requests.get('https://api.github.com/search/repositories?q=language:java')
print(repo)

if repo.status_code != 403:

    response=repo.json()
    for i in range(len(response['items'])):
        repo_name=response['items'][i]['full_name']

    #get all commit for a repo
        #head = {'Accept': 'application/vnd.github+json'}
        #commits = requests.get('https://api.github.com/search/commits?q=repo:'+repo_name,headers=head)

    #get all close pull requests for a repo
        print('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name)
        pull_req = requests.get('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name)
        print(pull_req.status_code)
        print(repo_name)
        print(len(pull_req.json()))
        print(pull_req.json())
        if pull_req.status_code == 200:
            pull_url = pull_req.json()["items"][0]["pull_request"]["url"]
            #[0]['head']['repo']['clone_url']
            print(pull_url)
            pull_req1 = requests.get(pull_url)
            clone_url = pull_req1.json()['head']['repo']['clone_url']
            #print('clone',clone_url)

            directory = "D:\\gitrepos\\"+repo_name
            if os.path.exists(directory):
                os.remove(directory)
            os.makedirs(directory)

            output = subprocess.check_output(
                "git clone {cloneUrl} {directoryPath}".format(cloneUrl=clone_url, directoryPath=directory),
                shell=True)

            logging.info(output)

            #getting commit history
            commits = []

#https://api.github.com/search/repos/ReactiveX/repo_name/pulls/

#https://api.github.com/repos/ReactiveX/RxJava/pulls/5938