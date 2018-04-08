# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import operator

#parse the xml tree and get the root element of the tree
tree = ET.parse("out.xml")
root = tree.getroot()

# All 'project' children of the top-level
child=root.findall("./project")

#global count for all issues
issue_count=dict()

#list of change types
change_type=['Austria','Costa','Costa Rica']

#update the global frequency for the change type
def update_count(i,name):
    result=i.findall(".//parameter/..[@name='"+name+"']")
    for j in range(len(result)):
        if name in issue_count:
            issue_count[name]+=1
        else:
            issue_count[name]=1

#find frequency of particular type of change across all projects
for node in child:
    for change in change_type:
        update_count(node,change)
  
#find top 5 maximum occuring changes for issues
top5 = dict(sorted(issue_count.items(), key=operator.itemgetter(1), reverse=True)[:5])
print(top5)

