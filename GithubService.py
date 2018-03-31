# -*- coding: utf-8 -*-

import requests

#get all java repo
repo = requests.get('https://api.github.com/search/repositories?q=language:java')
response=repo.json()
for i in range(len(response['items'])):
    repo_name=response['items'][i]['full_name']

#get all commit for a repo
    #head = {'Accept': 'application/vnd.github+json'}
    #commits = requests.get('https://api.github.com/search/commits?q=repo:'+repo_name,headers=head)

#get all close pull requests for a repo
    pull_req = requests.get('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name)
    print(pull_req.status_code)

