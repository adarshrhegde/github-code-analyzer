
# coding: utf-8

# In[100]:


import requests
import subprocess
import logging
from UnderstandService import create_udb,execute
from git import Repo
from github import Github
import understand
import  configparser 
import os
import shutil


config =  configparser.RawConfigParser()
config.read('GitHubVariables.properties') 
global number_of_projects
number_of_commits=config.get('Project','number_of_commits')
path=config.get('Project','project_path')


#github Authentication using token
headers={'Authorization':'token 5c4d81ec05cb82053d9fd0c0519120fe3eed17be',
        'User-Agent':'https://api.github.com/meta',
        'Content-Type':'application/json'}

global udb_path1
global udb_path2
global project_root1
global project_root2
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

    try:
        if pull_req.status_code == 200:
                pull2=pull_req.json()
                repo_url=pull2['items'][0]['repository_url']
                #print('Repo_URL:',repo_url)
                response=requests.get(repo_url,headers=headers)
                if pull_req.status_code == 200:
                    repo_url=response.json()['html_url']

    except IndexError as e:
        print('-----------------Exception occured while getting repo url---------------')
                
    return repo_url

def clone_repo(repo_url,name,num):
    try:
        git_url=repo_url
       
        repo_dir=path + name+'\\'+str(num)
        if os.path.isdir(repo_dir):
            os.system('rmdir /S /Q "{}"'.format(repo_dir))

        print('Cloning at:',repo_dir)
        Repo.clone_from(git_url, repo_dir)
        #print('Done cloning')
    except:
        print('Exception occured while cloneing repo', name)

    return repo_dir

#Checkout the version of the project using the SHA for that version
def git_checkout(sha,projectname,num,number_of_projects):
        
        result = []
        flag=True
        cmd='git checkout '+ sha
        
        process = subprocess.Popen(cmd,cwd=path+projectname+'\\'+str(num)+'\\',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE )
        result = process.communicate()[1].decode().split(':')[0]
        #print(result)
        if(result=="FATAL" or result=="fatal"):
            number_of_projects=number_of_projects+1
            flag=False
        return flag,number_of_projects
    
        
            

# Searches for closed issues for repositiories and gets list of pull requests.
# Further commit listnumber_of_projects is populated for the list of pullrequest and corresponding SHA of each commit is stored in sha_list
# Project from the repo is cloned in user defined Path from properties file
def git_analyzer():
    repo = requests.get('https://api.github.com/search/repositories?q=language:java',headers=headers)
    #Search for repositories with language:Java
    
    number_of_projects=int(config.get('Project','number_of_projects'))

    if repo.status_code != 403:

        response=repo.json()
        for i in range(number_of_projects):
            if int(len(response['items']))< number_of_projects:
                break
            repo_name=response['items'][i]['full_name']
            #repo_name='iluwatar/java-design-patterns'
            #print('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name)
            pull_req = requests.get('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:'+repo_name,headers=headers)
            commit_list=list()    

            projectname=repo_name.split("/")[1]
            print('Project name:',projectname)

            # get the repository URL
            repo_url=get_repo_url(pull_req)


            #Clone the repository
            repo_dir1=clone_repo(repo_url,projectname,1)
            repo_dir2=clone_repo(repo_url,projectname,2)


            #Create the UDB for the project

           
            udb_path1=repo_dir1
            udb_path2=repo_dir2
            
        

            #Get pull and commit list for the project
            commit_list=get_pull_req(pull_req)
            #print('commit list',commit_list)
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
            
            #return
            number_of_projects=process(sha_list,projectname,udb_path1,udb_path2,number_of_projects)

# The clone repo is then checked out to the SHA version and for every pair of consecutive versions,
# pair of udbs are created and processed usinf execute method
def process(sha_list,projectname,udb_path1,udb_path2,number_of_projects):
            #print(sha_list)
            #checkout to base version

            try:
                        flag,np=git_checkout(sha_list[len(sha_list)-1],projectname,1,number_of_projects)
                        flag,np=git_checkout(sha_list[len(sha_list)-1],projectname,2,number_of_projects)
                        project_root1=udb_path1
                        project_root2=udb_path2
                        if not flag:
                            return np
                        else:
                            print('Checkout successful')

                            
                        for l in range(int(number_of_commits)):
                            if int(len(sha_list))< int(number_of_commits):
                                break
                            
                          #  print(sha_list[len(sha_list)-l-1])
                            language='java'
                           
                            #Checkout the next version using SHA
                            flag,np=git_checkout(sha_list[len(sha_list)-l-2],projectname,1,number_of_projects) 
                            #Checkout the next version using SHA
                            flag,np=git_checkout(sha_list[len(sha_list)-l-3],projectname,2,number_of_projects)
                            
                            #Create analyze the UDB with the new code version
            #                print('Path',r''+udb_path1+r'\1')
                            
                            create_udb(r''+udb_path1+r'\1', language, project_root1)
                            create_udb(r''+udb_path2+r'\2', language, project_root2) 
                            path1=r''+udb_path1+r'\1.udb'
                            path2=r''+udb_path2+r'\2.udb'
                           
                            try:
                                db1 = understand.open(path1)
                                db2 = understand.open(path2) 
                            except understand.UnderstandError as e:
                                logging.fatal('udb open failed')
                                raise Exception
                            #Executing Understand analysis 
                            execute(db1,db2,projectname, '1')
                            
                            db1.close()
                            db2.close()
            except:
                print('Exception occured during processing')
                return 0
                return np


#git_analyzer()
#Kill Switch

        


# In[89]:




