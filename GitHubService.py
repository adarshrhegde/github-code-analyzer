
# coding: utf-8

# In[20]:


import requests
import subprocess
import logging
import os
from UnderstandService import create_udb,execute
from git import Repo
from github import Github
import understand
import  configparser 
config =  configparser.RawConfigParser()
config.read('GitHubVariables.properties') 
number_of_projects=config.get('Project','number_of_projects')
number_of_commits=config.get('Project','number_of_commits')
path=config.get('Project','project_path')
print(number_of_commits)


#github Authentication using token
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

#Checkout the version of the project using the SHA for that version
def git_checkout(sha,projectname):
        print('Checking out for',sha)
        result = []
        cmd='git checkout '+ sha
        print(cmd)
        print(path+projectname+'\\')
        process = subprocess.Popen(cmd,cwd=path+projectname+'\\',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE )

        for line in process.stdout:
            result.append(line)
            errcode = process.returncode
        for line in result:
            print(line)

# Searches for closed issues for repositiories and gets list of pull requests.
# Further commit list is populated for the list of pullrequest and corresponding SHA of each commit is stored in sha_list
# Project from the repo is cloned in user defined Path from properties file
def git_analyzer():
    repo = requests.get('https://api.github.com/search/repositories?q=language:java',headers=headers)
    #Search for repositories with language:Java
    print(repo)

    if repo.status_code != 403:

        response=repo.json()
        for i in range(int(number_of_projects)):
            if int(len(response['items']))< int(number_of_projects):
                break
            repo_name=response['items'][i]['full_name']
            print('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name)
            pull_req = requests.get('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name,headers=headers)
            commit_list=list()    

            projectname=repo_name.split("/")[1]
            print('Project name:',projectname)

            # get the repository URL
            repo_url=get_repo_url(pull_req)
            print('Repo_url',repo_url)


            #Clone the repository
            repo_dir=clone_repo(repo_url,projectname)


            #Create the UDB for the project

            print(projectname)
            udb_path=repo_dir
            language='java'
            project_root=repo_dir

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
            process(sha_list,projectname,udb_path,project_root)

# The clone repo is then checked out to the SHA version and for every pair of consecutive versions,
# pair of udbs are created and processed usinf execute method
def process(sha_list,projectname,udb_path,project_root):
            git_checkout(sha_list[0],projectname) # Checking out repo to get Base version

            for l in range(int(number_of_commits)):
                if int(len(sha_list))< int(number_of_commits):
                    break
                print(sha_list[len(sha_list)-l-1])
                language='java'
                create_udb(udb_path+'1', language, project_root)     

    #Checkout the next version using SHA
                git_checkout(sha_list[len(sha_list)-l-1],projectname)
        #analyze the UDB with the new code version
                create_udb(udb_path+'2', language, project_root) 
                print(udb_path)
                db1 = understand.open(r''+udb_path+'1.udb')
                db2 = understand.open(r''+udb_path+'2.udb')                
                execute(db1,db2,projectname, project_root)
                print("Execute called")
                db1.close()
                db2.close()



git_analyzer()


        

