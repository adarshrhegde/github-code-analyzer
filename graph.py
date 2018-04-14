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
#            print("kind",ent.kind())
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

G = nx.Graph()
db = understand.open("C:\\Users\\ashwa\\MyUnderstandProject8.udb")
class1 = db.lookup("com.uic.atse.service.GithubService","class")[0]
print("class name",class1.longname())
G.add_node(class1.longname(),entity=class1)

create_graph_node(G, class1)
nx.draw(G)
nx.draw_random(G)
nx.draw_circular(G)
nx.draw_spectral(G)
#nx.draw_graphviz(G)