# -*- coding: utf-8 -*-
"""

Service Fetch understand metadata data (entities and relationships, lexemes )

"""

import understand
db = understand.open("C:\\Users\\ashwa\\MyUnderstandProject1.udb")

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

file = db.lookup('hub',"file")[0]
file = db.lookup('GithubService.java')[0]
for lexeme in file.lexer():
    print (lexeme.text(),end="")
    if lexeme.ent():
        print('The lexeme entity kind is :' + str(lexeme.ent().kind()))
        print('The lexeme entity type is  :' + str(lexeme.ent().type()))
    else:
        print('The lexeme entity token is  :' + str(lexeme.token()))
    
        
#all information about the Functions
#for func in db.ents("function,method,procedure"):
#  for line in func.ib():
#    print(line,end="")