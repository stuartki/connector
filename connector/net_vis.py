from network import init
import networkx as nx 
from pyvis.network import Network
from Node import Node

def net_vis(data):
    
    def mark(node, data, DG):
        for x in node.past:
            if x == '':
              continue
            DG.add_node(data[int(x)].id, title = data[int(x)].title)
            DG.add_edge(data[int(x)].id, node.id)
        for x in node.future:
            if x == '':
                continue
            DG.add_node(data[int(x)].id, title = data[int(x)].title)
            DG.add_edge(node.id, data[int(x)].id)

    DG = Network(directed = True)	
    for node in data:
        if type(node) != Node:
            continue
        else:
            DG.add_node(node.id, title = node.title)
            mark(node, data, DG)
    DG.show("mygraph.html")
    return DG



if __name__ == "__main__":
    topic = "probability"
    from reader import reader
    from network import init
    data = reader(topic)
    DG = init(data)
    net_vis(data)