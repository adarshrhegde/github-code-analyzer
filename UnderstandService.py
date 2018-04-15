# -*- coding: utf-8 -*-
"""

Service Fetch understand metadata data (entities and relationships, lexemes )
and analyzes the patches 

"""

import understand
import diff
import xml.etree.ElementTree as ET
import subprocess
import logging
import graph as g

""""
Get the modifications done for the lexemes 
"""""

def getModifications(lexeme_context,lexeme_context_new):
    list_changes=[]
    for key in lexeme_context.keys():
        if key in lexeme_context_new.keys():
            if(len(lexeme_context[key])>1):
                if(lexeme_context[key][1]==lexeme_context_new[key][1]):
                    if(lexeme_context[key][0]!=lexeme_context_new[key][0]):
                        list_changes.append((key,str(lexeme_context[key][0]),str(lexeme_context_new[key][0]),"modified"))
        else:
            list_changes.append((str(lexeme_context[key][0]),"deleted"))
    for key in lexeme_context_new.keys():
        if key not in lexeme_context.keys():
            list_changes.append((key,str(lexeme_context_new[key][0]),"added"))
    return list_changes

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
Get all lexemes and tokens for a file 
"""""

def getLexemes(db,file_name,kind_dict,type_dict,token_dict,lexeme_context,loop_context):
    file = db.lookup(file_name)[0]
    list1 = []
    for lexeme in file.lexer():
        list1.append(lexeme.text())
        if(str(lexeme.previous())!='None'):
        #getting variable declaration changes     
            if(str(lexeme.previous().token()) in ('Whitespace','Punctuation')):
                if(str(lexeme.previous().previous())!='None'):
                    lexeme_context[lexeme.text()]=[lexeme.previous().previous().text()]
                else:
                    lexeme_context[lexeme.text()]=[lexeme.previous().text()]
                    
        #getting loops condition changes:
        loop_constructs={'if','for','while'}
        getcondtion=""
        if(lexeme.text() in loop_constructs):
            next_lexeme=lexeme.next()
            while(lexeme.next()!='None' and next_lexeme.text()!=')'):
                next_lexeme=next_lexeme.next()
                if(not next_lexeme.text()==')'):
                    getcondtion+=next_lexeme.text()
            loop_context[lexeme.text()]=[getcondtion]
            loop_context[lexeme.text()].append(lexeme.line_begin())


        if lexeme.ent():
            kind_dict[lexeme.text()] = lexeme.ent().kind();
            type_dict[lexeme.text()] = lexeme.ent().type();
            if(lexeme.ent().type()!='NoneType'):
                for eref in lexeme.ent().refs():
                    if lexeme.text() in lexeme_context.keys():
                        lexeme_context[lexeme.text()].append(eref.line()) 
        else:
            if(str(lexeme.token()) not in ('Whitespace','Punctuation','Newline')):
                token_dict[lexeme.text()] = lexeme.token()
                if lexeme.text() in lexeme_context.keys():
                    lexeme_context[lexeme.text()].append(lexeme.line_begin())
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

    file_deleted=file_set1.difference(file_set2)
    file_added=file_set2.difference(file_set1)
   
    for file in file_added:
        file2 = db2.lookup(file,"file")[0]    
        class10 = [sel_class for sel_class in db2.lookup(file.split(".")[0],"class") if sel_class.parent() == file2][0]
        class_elem = ET.SubElement(root, "class")
        class_elem.set("name",class10.simplename())
        class_elem.set("type","Added")
        class_elem.set("name","class")

    
    for file in file_deleted:
        file1 = db.lookup(file,"file")[0]
        class10 = [sel_class for sel_class in db.lookup(file.split(".")[0],"class") if sel_class.parent() == file1][0]
        class_elem = ET.SubElement(root, "class")
        class_elem.set("name",class10.simplename())
        class_elem.set("type","deleted")
        class_elem.set("name","class")

      
    if(not (bool(filenames))):
        print('No changes done')
        
        
    for file in filenames:
        class_elem = ET.SubElement(root, "class")
        class_elem.set("name",file)

        g.generate(db,db2,file, class_elem)
        analyze(db,db2,name,file,class_elem)

    tree = ET.ElementTree(root)
    tree.write("changes.xml")	


""" Analyze the diff using two understand database objects
	Pick up the common files in each database and get the diff to identify changes
	Once the diff code has been identified analyze the entities that are part of it
	With this information populate the xml 
"""
def analyze(db,db2,name,file_name,class_elem):
	
    accepted_token_types = ['Keyword']
    kind_dict = {}
    type_dict = {}
    token_dict = {}
    lexeme_context={}
    lexeme_context_new={}
    loop_context={}
    loop_context_new={}
    data_types={'int','char','float','double','long','short','byte','boolean'}

    xml_elements = xml_elements_from_props()
    print("Analyzing"+str(file_name))
    list1=[]
    list1=getLexemes(db,file_name,kind_dict,type_dict,token_dict,lexeme_context,loop_context)
    list2=getLexemes(db2,file_name,kind_dict,type_dict,token_dict,lexeme_context_new,loop_context_new)
    diff_result = diff.diff_result(list1,list2)
    for key in diff_result:
        val = diff_result[key][2:]
        sign = diff_result[key][0:1]
        if val in token_dict:
            if token_dict[val] in accepted_token_types:
                if sign=='+':
                    status="Added"
                elif sign=='-':
                    status="Removed"
                if val in xml_elements:
                    elem = ET.SubElement(class_elem, "change")
                    token_elem = ET.SubElement(elem,xml_elements[val])
                    elem.set("type",status)
                    elem.set("name",val)

    changes=getModifications(lexeme_context,lexeme_context_new)
    changes_loops=(getModifications(loop_context,loop_context_new))

    loop_constructs={'if','for','while','do'}
    for change in changes_loops:
        if(change[0] in loop_constructs and change[len(change)-1]!='modified'):
            elem = ET.SubElement(class_elem, "change")
            param = ET.SubElement(elem, change[0]+"statement")
            param.set("addcondition","True")
            if(change[0]=='for'):
                param.set("condition",change[1].split(';')[1])
            elem.set("type",change[len(change)-1])
            elem.set("name",change[0]+"statement")
            
        elif(change[len(change)-1]=='modified'):
            elem1 = ET.SubElement(class_elem, "change")
            param1 = ET.SubElement(elem1, change[0]+"statement")
            param1.set("changecondition","True")
            param1.set("condition",change[2])
            elem1.set("type",change[len(change)-1])
            elem.set("name",change[0]+"statement")
            
    for change in changes:   
        if(change[0] in data_types and change[1] in data_types):
            elem = ET.SubElement(class_elem, "change")
            param = ET.SubElement(elem, "parameter")
            param.set("oldType",change[0])    
            param.set("newType",change[1])
            elem.set("type","Modified")
            elem.set("name","variableDefinition")
        
        if(change[0] in data_types and change[1]=="added"):
            elem = ET.SubElement(class_elem, "change")
            param = ET.SubElement(elem, "parameter")
            param.set("oldType","None")    
            param.set("newType",change[0])
            elem.set("type","Added")        
            elem.set("name","variableDefinition")
 
        if(change[0] in data_types and change[1]=="deleted"):
            elem = ET.SubElement(class_elem, "change")
            param = ET.SubElement(elem, "parameter")
            param.set("oldType",change[0])    
            param.set("newType","None")
            elem.set("type","Deleted")
            elem.set("name","variableDefinition")
 

