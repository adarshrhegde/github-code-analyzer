
# coding: utf-8

# In[1]:


print ('Hello')


# In[7]:


import subprocess
import logging

def create_udb(udb_path, language, project_root):
    try:
        output = subprocess.check_output(
            "und create -db {udb_path} -languages {lang}".format(udb_path=udb_path, lang=language),
            shell=True)
        logging.info(output)
        output = subprocess.check_output("und add -db {udb_path} {project}".format(
            udb_path=udb_path, project=project_root), shell=True)
        logging.info(output)
    except subprocess.CalledProcessError as e:
        logging.exception(e.output)
        logging.fatal("udb creation failed")
        raise Exception

create_udb('C:\\Understand\\Proj1.udb','java',r'D:\\git\\adarsh_hegde_ashwani_khemani_srinath_kv_hw1')


# In[9]:

'''
import urllib.request, json 
f= urllib.request.urlopen("https://api.github.com/search/repositories?q=topic:java")
data = json.load(f)
f.close()
URL=[]
description=[]
for i in range (0, len (data['items'])):
    URL.append(data['items'][i]['svn_url'])
    description.append(data['items'][i]['name'])

print(URL)
print(description)
'''



# In[4]:





# In[11]:


print("Finito")

