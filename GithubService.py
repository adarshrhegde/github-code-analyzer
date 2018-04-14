
# coding: utf-8

# In[42]:


import requests
import subprocess
import logging
import os
from UnderstandService import create_udb,execute
from git import Repo
from github import Github

import  configparser 
config =  configparser.RawConfigParser()
config.read('C:\\Users\\Srinath\\Desktop\\HW2\\GitHubVariables.properties') 
number_of_projects=config.get('Project','number_of_projects')
number_of_commits=config.get('Project','number_of_commits')
path=config.get('Project','project_path')


# In[58]:


headers={'Authorization':'token 5c4d81ec05cb82053d9fd0c0519120fe3eed17be',
        'User-Agent':'https://api.github.com/meta',
        'Content-Type':'application/json'}
global udb_path
global project_root
global repo_name
global projectname

def get_pull_req(pull_req):   # Getting the list of pull requests to get all commit requests
    commit_list=list()
    repo_pulls=list()
    if pull_req.status_code == 200:
        pull2=pull_req.json()
        for j in range(len(pull2['items'])):
                repo_pulls.insert(j,pull2['items'][j]['pull_request']['url'])
                commit=repo_pulls[j] + '/commits'
                #print('get_pull_req',commit)
                commit_list.insert(j,commit)
    return commit_list         
    
def get_repo_url(pull_req)    : # Get the repo URL to clone the repo
    repo_url=''
    if pull_req.status_code == 200:
            pull2=pull_req.json()
            repo_url=pull2['items'][0]['repository_url']
            print(repo_url)
            response=requests.get(repo_url,headers=headers)
            if pull_req.status_code == 200:
                repo_url=response.json()['html_url']
            
    return repo_url

def clone_repo(repo_url,name):
    print('Done')
    git_url=repo_url
   
    repo_dir=path + name+'\\'
    Repo.clone_from(git_url, repo_dir)
    print('Done cloning')
    return repo_dir

def git_checkout(sha):
        print('Checking out for',sha)
        result = []
        cmd='git checkout '+ sha
        print(cmd)
        process = subprocess.Popen(cmd,cwd=path+projectname+'\\',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE )

        for line in process.stdout:
            result.append(line)
            errcode = process.returncode
        for line in result:
            print(line)


repo = requests.get('https://api.github.com/search/repositories?q=language:java',headers=headers)
print(repo)

if repo.status_code != 403:

    response=repo.json()
    for i in range(int(number_of_projects)):
        print()
        if int(len(response['items']))< int(number_of_projects):
            print(int(len(response['items'])))
            print(int(number_of_projects))            
            break
        repo_name=response['items'][i]['full_name']
        print('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name)
        pull_req = requests.get('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name,headers=headers)
        commit_list=list()
        
        


# In[44]:



projectname=repo_name.split("/")[1]
print(projectname)

# get the repository URL
repo_url=get_repo_url(pull_req)
print('Repo_url',repo_url)



# In[52]:


#Clone the repository
repo_dir=clone_repo(repo_url,projectname)


# In[ ]:



#Create the UDB for the project
projectname=repo_name.split("/")[1]
print(projectname)
udb_path=repo_dir
language='java'
project_root=repo_dir
       # create_udb(udb_path, language, project_root)

#Get pull and commit list for the project
commit_list=get_pull_req(pull_req)
sha_list=list()
#Iterating through list of commits to get the SHAs 
for j in range(len(commit_list)):
    commit_json=requests.get(commit_list[j]+'',headers=headers)
   # print('length=',(len(commit_json.json())))
    for k in range(len(commit_json.json())): 
        
         #Iterating through list of commits for SHA 
        if commit_json.status_code == 200:
            if(len(commit_json.json())==1):
                sha_list.append(commit_json.json()[k]['sha'])
                
            else:
                sha_list.append(commit_json.json()[(len(commit_json.json()))-k-1]['sha'])
                

            
#print('length=',len(sha_list))
git_checkout(sha_list[0]) # Checking out repo to get Base version

for l in range(len(sha_list)):
    if int(len(sha_list))< int(number_of_commits):
        break
    print(sha_list[len(sha_list)-l-1])
    language='java'
    print('udb_path',udb_path)
    print('project_root',project_root)
    projectname=repo_name.split("/")[1]
    print(projectname)
    import understand
    
    create_udb(udb_path+'1', language, project_root)     

#Checkout the next version using SHA
    git_checkout(sha_list[len(sha_list)-l-1])
    #analyze the UDB with the new code version
    create_udb(udb_path+'2', language, project_root) 
                    


# In[ ]:




    db1 = understand.open(udb_path+'\1.udb')
    db2 = understand.open(udb_path+'\2.udb')                
    #execute(db1,db2,projectname, project_root)
    print("Execute called")
    db1.close()
    db2.close()

   

