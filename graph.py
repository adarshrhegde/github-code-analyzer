

import sys

import understand

import networkx as nx


"""
Used to create graphs for entities to better analyze changes

"""

"""
Create graph nodes in a recursive fashion
"""
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


"""
Create single graph object
"""
def create_graph():
    G = nx.Graph()
    return G
