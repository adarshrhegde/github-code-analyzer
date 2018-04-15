# -*- coding: utf-8 -*-

#Service to find the most common changes across all projets #

import xml.etree.ElementTree as ET
import operator

#parse the xml tree and get the root element of the tree
tree = ET.parse("changes.xml")
root = tree.getroot()

#print(root)
# All 'project' children of the top-level
child=root.findall("./")
#print(child)
#global count for all issues
issue_count=dict()

#list of change types
change_type=['objectCreation','tryblock','catchBlock','throwstatement','switchstatement','inheritance',
             'dependency','variableDefinition','ifstatement','forstatement',
             'whilestatement','dostatement','method','class']

#update the global frequency for the change type
def update_count(i,name):
    result=i.findall(".//change[@name='"+name+"']")
    print(result)
    for j in range(len(result)):
        if name in issue_count:
            issue_count[name]+=1
        else:
            issue_count[name]=1

#find frequency of particular type of change across all projects
for node in child:
    print(node)
    for change in change_type:
        update_count(node,change)
  
#find top 5 maximum occuring changes for issues
top5 = dict(sorted(issue_count.items(), key=operator.itemgetter(1), reverse=True)[:5])
print(top5)

