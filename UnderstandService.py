# -*- coding: utf-8 -*-
"""

Service Fetch understand metadata data (entities and relationships, lexemes )

"""

import understand
import diff
import xml.etree.ElementTree as ET
import subprocess
import logging
import graph as g


"""
Create a understand database from the source code
"""
def create_udb(udb_path, language, project_root):
	try:
		output = subprocess.check_output("und create -db {udb_path} -languages {lang}".format(udb_path=udb_path, lang=language),shell=True)
		logging.info(output)
		output = subprocess.check_output("und add -db {udb_path} {project}".format(udb_path=udb_path, project=project_root), shell=True)
		logging.info(output)
		output = subprocess.check_output("und analyze {udb_path}".format(udb_path=udb_path), shell=True)
		logging.info(output)
	except subprocess.CalledProcessError as e:
		logging.exception(e.output)
		logging.fatal("udb creation failed")
		raise Exception

#create_udb("C:\\Understand\\v10.udb",'java',"D:\\versions\\1\\adarsh_hegde_ashwani_khemani_srinath_kv_hw1")
#create_udb("C:\\Understand\\v11.udb",'java',"D:\\versions\\2\\adarsh_hegde_ashwani_khemani_srinath_kv_hw1")

"""""
get all lexemes and tokens for a file 
"""""
def getLexemes(db,file_name,kind_dict,type_dict,token_dict):
    file = db.lookup(file_name)[0]
    list1 = []
    for lexeme in file.lexer():

        list1.append(lexeme.text())

        if lexeme.ent():
            kind_dict[lexeme.text()] = lexeme.ent().kind();
            type_dict[lexeme.text()] = lexeme.ent().type();
#            print('The lexeme entity kind is :' + str(lexeme.ent().kind()))
#            print('The lexeme entity type is  :' + str(lexeme.ent().type()))
        else:
            token_dict[lexeme.text()] = lexeme.token()
#            print('The lexeme entity token is  :' + str(lexeme.token()))
    return list1


""" Gets entity-xml_name mapping from properties file
	For eg. entity 'if' is represented as 'ifstatement' in the xml

"""
        
def xml_elements_from_props():
	myprops = {}
	with open('elements.properties', 'r') as f:
	    for line in f:
	        line = line.rstrip() #removes trailing whitespace and '\n' chars

	        if "=" not in line: continue #skips blanks and comments w/o =
	        if line.startswith("#"): continue #skips comments which contain =

	        k, v = line.split("=", 1)
	        myprops[k] = v
	return myprops

def sortKeyFunc(ent):
  return str.lower(ent.longname())
 
def analyze_functions(db):
	ents = db.ents("function,method,procedure")
	for func in sorted(ents,key = sortKeyFunc):
	  print (func.longname()," (",sep="",end="")
	  first = True
	  for param in func.ents("Define","Parameter"):
	    if not first:
	      print (", ",end="")
	    print (param.type(),param,end="")
	    first = False
	  print (")")


"""
Returns a list of all filenames of given type
"""
def get_filenames(db, type, pkg_structure):

	filenames = set()
	size = len(type)
	for entity in db.ents():
		if entity.longname()[(-1*size):]==type:
			#and pkg_structure in entity.longname()
			filenames.add(entity.name())

	return filenames

"""

This function creates a template for the xml 
It creates nodes for different files in a project 
Then it does the analysis on the changed files 
"""

def execute(db,db2,name, pkg_structure):
    root = ET.Element("project")
    root.set("name",name)
    file_set1 = get_filenames(db,'.java',pkg_structure)
    file_set2 = get_filenames(db2, '.java',pkg_structure)
    filenames = set.intersection(file_set1,file_set2)

    if(not (bool(filenames))):
        print('No changes done')
        
        
    for file in filenames:
        class_elem = ET.SubElement(root, "class")
        class_elem.set("name",file)

        g.generate(db,db2,file, class_elem)
        analyze(db,db2,name,file,class_elem)
        graph.generate(db,db2,file,class_elem)

    tree = ET.ElementTree(root)
    tree.write("changes.xml")	


""" Analyze the diff using two understand database objects
	Pick up the common files in each database and get the diff to identify changes
	Once the diff code has been identified analyze the entities that are part of it
	With this information populate the xml 
"""
def analyze(db,db2,name,file_name,class_elem):
	
	#token_types = dict_values(['Keyword', 'Whitespace', 'Identifier', 'Punctuation', 'Identifier', 'Punctuation', 'Newline', 'Keyword', 'Identifier', 'Keyword', 'Keyword', 'Punctuation', 'Whitespace', 'Keyword', 'Keyword', 'Punctuation', 'Punctuation', 'Punctuation', 'Punctuation', 'Whitespace', 'Operator', 'Punctuation', 'Whitespace', 'Keyword', 'Keyword', 'Operator', 'Whitespace', 'String'])
    accepted_token_types = ['Keyword']
    kind_dict = {}
    type_dict = {}
    token_dict = {}

    xml_elements = xml_elements_from_props()

    list1=getLexemes(db,file_name,kind_dict,type_dict,token_dict)
    list2=getLexemes(db2,file_name,kind_dict,type_dict,token_dict)
    diff_result = diff.diff_result(list1,list2)
#    print((diff_result))
    for key in diff_result:
        val = diff_result[key][2:]
        sign = diff_result[key][0:1]

        if val in token_dict:
            if token_dict[val] in accepted_token_types:
                if sign=='+':
                    print("Added")
                    status="Added"
                elif sign=='-':
                    print("Removed")
                    status="Removed"
#				print("token>>",val)
                if val in xml_elements:
                    elem = ET.SubElement(class_elem, "change")
                    token_elem = ET.SubElement(elem,xml_elements[val])
                    elem.set("name",status)
                else: 
                    if sign=='+':
                        print("Added")
                    elif sign=='-':
                        print("Removed")
#			print("entity>>",val)
#			print("kind>>",kind_dict[val])
#			print("type>>",type_dict[val])


'''
print(db.ents())
for ent in sorted(db.ents(),key= lambda ent: ent.name()):
  print (ent.name(),"  [",ent.kindname(),"]",sep="",end="\n")
'''
'''
for func in db.ents("function,method,procedure"):
  file = "D:\\git\\adarsh_hegde_ashwani_khemani_srinath_kv_hw2\\result\\callby_" + func.name() + ".png"
  print (func.longname(),"->",file)
  func.draw("Called By",file)

print(db.ents("Global Object ~Static"))
for ent in db.ents("Global Object ~Static"):
  print (ent,":",sep="")
  for ref in ent.refs():
    print (ref.kindname(),ref.ent(),ref.file(),"(",ref.line(),",",ref.column(),")")
  print ("\n",end="")


''' 

	
#db6 = understand.open("C:\\Understand\\v6.udb")
#db7 = understand.open("C:\\Understand\\v2.udb")
# for entity in db.ents():
# 	if '.java' in entity.name():
# 		print(entity.longname())

#execute(db6, db7, 'Dev-ops','ASE')
#db6.close() 
#db7.close() 
#create_udb("C:\\Understand\\v6.udb", "java", "C:\\adarsh_hegde_ashwani_khemani_srinath_kv_hw1")
#analyze_functions(db)

'''        
#all information about the Functions
#for func in db.ents("function,method,procedure"):
#  for line in func.ib():
#    print(line,end="")
'''