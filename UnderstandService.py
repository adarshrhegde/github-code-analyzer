# -*- coding: utf-8 -*-
"""

Service Fetch understand metadata data (entities and relationships, lexemes )

"""

import understand
import diff
db = understand.open("C:\\Understand\\Proj2.udb")
db2 = understand.open("C:\\Understand\\Proj2-mod.udb")

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


file = db.lookup('Main.java')[0]
#print(file.lexer())
list1 = []
for lexeme in file.lexer():
    #print (lexeme.text(),end="")
    list1.append(lexeme.text())
    """
                if lexeme.ent():
                    print('The lexeme entity kind is :' + str(lexeme.ent().kind()))
                    print('The lexeme entity type is  :' + str(lexeme.ent().type()))
                else:
                    print('The lexeme entity token is  :' + str(lexeme.token()))
            """

file2 = db2.lookup('Main.java')[0]
#print(file.lexer())
list2 = []
for lexeme in file2.lexer():
    #print (lexeme.text(),end="")
    list2.append(lexeme.text())

#print(list1)

print()
#print(list2)

print(diff.diff_result(list1,list2))
'''        
#all information about the Functions
#for func in db.ents("function,method,procedure"):
#  for line in func.ib():
#    print(line,end="")
'''