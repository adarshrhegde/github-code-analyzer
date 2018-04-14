

import sys

import understand

import networkx as nx

import UnderstandService as us


"""
Used to create graphs for entities to better analyze changes

"""

# create a graph node for an entity and populate its child nodes
def create_graph_node(G, my_node):
    for ent in db.ents():
        if ent.parent() !=None and ent.parent().longname() == my_node.longname() :
            #print("kind",ent.kind())
            G.add_node(ent.longname(), entity=ent)
            G.add_edge(my_node.longname(),ent.longname(), relationship=ent.kind())
            #print("ent",ent.longname(),"kind",G[my_node.longname()][ent.longname()]["relationship"])
            create_graph_node(G, ent)
    
    

"""
Create single graph node
"""
def create_single_node(G, my_node):
    G.add_node(my_node.longname(),entity=my_node)    


# create a graph
def create_graph():
    G = nx.Graph()
    return G

# create a class node
def create_class_node(G,db,class_ent):
    G.add_node(class_ent.longname(),entity=class_ent)
    create_graph_node(G, class_ent)

# compare identical method nodes in two graphs
def compare_method_nodes(G1, G2, common_methods):
    for method in common_methods:
        print('Method', method)
        #Compare the parameters
        parameter_1 = [parameter for parameter in G1.neighbors(method) if G1[method][parameter]['relationship'].name() == 'Parameter']
        parameter_2 = [parameter for parameter in G2.neighbors(method) if G2[method][parameter]['relationship'].name() == 'Parameter']
        
        parameter_not_2 = [parameter for parameter in parameter_1 if parameter not in parameter_2]
        print("Parameter not in version 2", parameter_not_2)
        parameter_not_1 = [parameter for parameter in parameter_2 if parameter not in parameter_1]
        print("Parameter not in version 1", parameter_not_1)


# compare methods within a class
def compare_class_methods(G1, G2, class_name1, class_name2):    
    methods_1 = [method_node for method_node in G1.neighbors(class_name1) if "Method" in G1[class_name1][method_node]['relationship'].name()]
    methods_2 = [method_node for method_node in G2.neighbors(class_name2) if "Method" in G2[class_name2][method_node]['relationship'].name()]
    
    only_methods_1 = [x for x in methods_1 if x not in methods_2]
    print("Methods only in 1", only_methods_1)
    only_methods_2 = [x for x in methods_2 if x not in methods_1]
    print("Methods only in 2", only_methods_2)
    common_methods = [x for x in methods_1 if x in methods_2]
    
    return common_methods



db = understand.open("C:\\Understand\\v6.udb")
db2 = understand.open("C:\\Understand\\v3.udb")


files1 = us.get_filenames(db, '.java', '')
files2 = us.get_filenames(db2, '.java', '')
filenames = list(set.intersection(files1,files2))

for filename in filenames:
    file1 = db.lookup(filename,"file")[0]
    file2 = db2.lookup(filename,"file")[0]
    #print((file1.name()))
    #print((file2.name()))
    class10 = [sel_class for sel_class in db.lookup(filename.split(".")[0],"class") if sel_class.parent() == file1][0]
    class11 = [sel_class for sel_class in db2.lookup(filename.split(".")[0],"class") if sel_class.parent() == file2][0]
    #print("class10",class10)
    #print("class11",class11.longname())
    class_name1 = class10.longname()
    class_name2 = class11.longname()
    G1 = create_graph()
    G2 = create_graph()
    create_class_node(G1, db, class10)
    create_class_node(G2, db2, class11)
    #print(G2.nodes())
    common_methods = compare_class_methods(G1, G2, class_name1, class_name2)


    compare_method_nodes(G1, G2, common_methods)


db.close()
db2.close()