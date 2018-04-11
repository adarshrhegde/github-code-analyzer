# -*- coding: utf-8 -*-
"""

Service Fetch understand metadata data (entities and relationships, lexemes )

"""

import understand
import diff
import xml.etree.ElementTree as ET

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


def execute(db,db2,name, pkg_structure):
	root = ET.Element("project")
	root.set("name",name)
	file_set1 = get_filenames(db,'.java',pkg_structure)
	file_set2 = get_filenames(db2, '.java',pkg_structure)
	filenames = set.intersection(file_set1,file_set2)

	for file in filenames:
		class_elem = ET.SubElement(root, "class")
		class_elem.set("name",file)
		analyze(db,db2,name,file,class_elem)

	
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

	file = db.lookup(file_name)[0]

	list1 = []
	for lexeme in file.lexer():

		list1.append(lexeme.text())

		if lexeme.ent():
			kind_dict[lexeme.text()] = lexeme.ent().kind();
			type_dict[lexeme.text()] = lexeme.ent().type();
		    #print('The lexeme entity kind is :' + str(lexeme.ent().kind()))
		    #print('The lexeme entity type is  :' + str(lexeme.ent().type()))
		else:
			token_dict[lexeme.text()] = lexeme.token()
		#print('The lexeme entity token is  :' + str(lexeme.token()))
		        

	file2 = db2.lookup(file_name)[0]
	#print(file.lexer())
	list2 = []
	for lexeme in file2.lexer():
		list2.append(lexeme.text())

		if lexeme.ent():
			kind_dict[lexeme.text()] = lexeme.ent().kind();
			type_dict[lexeme.text()] = lexeme.ent().type();
		 
		else:
			token_dict[lexeme.text()] = lexeme.token()

		#print(type_dict.keys(),type_dict.values())
	print(token_dict.keys(),token_dict.values())
		#print(list2)

	diff_result = diff.diff_result(list1,list2)

	print(type(diff_result))
	for key in diff_result:
		val = diff_result[key][2:]
		sign = diff_result[key][0:1]


		if val in token_dict:
			if token_dict[val] in accepted_token_types:
				if sign=='+':
					print("Added")
				elif sign=='-':
					print("Removed")
				print("token>>",val)
				if val in xml_elements:
					elem = ET.SubElement(class_elem, "change")
					token_elem = ET.SubElement(elem,xml_elements[val])
					#token_elem.set("addCondition","true")
		else: 
			if sign=='+':
				print("Added")
			elif sign=='-':
				print("Removed")
			print("entity>>",val)
			print("kind>>",kind_dict[val])
			print("type>>",type_dict[val])


#entities which are class or function

#for file in db.ents("class,function"):
#    print(file.longname())

#sorted list of all entities

#for ent in sorted(db.ents(),key= lambda ent: ent.name()):
#  print (ent.name(),"  [",ent.kindname(),"]",sep="",end="\n")

  
#fetch functions , method , procedure and their entity type  

#ents = db.ents("function,method,procedure")
#for ent in sorted(db.ents(""),key= lambda ent: ent.longname()):
#    ref = ent.ref("definein");
#    print (ent.longname(),"(",ent.parameters(),")", ent.kindname());
#    if ref is None:
#        continue;
#    print (ent.longname(),"(",ent.parameters(),")");
#    print ("  ",ref.file().relname(),"(",ref.line(),")");


# =============================================================================
# find all lexemes and the entity kind,type,token type for a file
# kind : class , variable
# type : eg class of the object
# returns the information about entities which are defined by understand
# and for non-entites it returns the token type
# lexeme.text : gives the actual instance of the entity
# =============================================================================

#file = db.lookup('hub',"file")[0]
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

	
db = understand.open("C:\\Understand\\Proj2.udb")
db2 = understand.open("C:\\Understand\\Proj2-mod.udb")
# for entity in db.ents():
# 	if '.java' in entity.name():
# 		print(entity.longname())

#execute(db, db2, 'Dev-ops','abv')

#analyze_functions(db)

'''        
#all information about the Functions
#for func in db.ents("function,method,procedure"):
#  for line in func.ib():
#    print(line,end="")
'''