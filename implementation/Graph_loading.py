import networkx as nx
from tqdm import tqdm
import random


'''
Function convert_to_undirected is used to convert directed graph to undirected.
If there is at least one negative edges between two nodes, edge between those two nodes in undirected graph will have negative affinity 
'''



def convert_to_undirected(graph):
    undirected_graph = nx.Graph()
    undirected_graph.add_edges_from(graph.edges(), affinity="")
    for u, v, d in graph.edges(data=True):
        aff1 = graph[u][v]['affinity']
        aff2 = ""
        if (v, u) in graph.edges:
            aff2 = graph[v][u]['affinity']
        if aff1 == "-" or aff2 == "-":
            undirected_graph[u][v]['affinity'] = "-"
        else:
            undirected_graph[u][v]['affinity'] = "+"
    return undirected_graph



'''
Function load_small_graph is used for loading a small graph and adding affinities on its edges.
'''



def load_small_graph():
    graph = nx.tutte_graph()
    add_affinity_on_edges(graph)
    return graph



'''
Function add_affinity_on_edges is used for adding affinites on edges without them. There is 33% chance for an endge to change from positive to negative
affinity 
'''



def add_affinity_on_edges(graph:nx.Graph):
    nx.set_edge_attributes(graph,"+","affinity")
    for node in graph:
        for second_node in graph:
            if node == second_node:
                continue
            if graph.has_edge(node,second_node):
                chance = random.random() > 0.66
                if chance :
                    graph.edges[node,second_node]['affinity'] = '-'



'''
Function load_wiki loads a wiki-RfA graph that is in form of a textual file
'''



def load_wiki(path):
    graph = nx.DiGraph()
    with open(path, "r", encoding="utf8") as file:
        source = None
        target = None
        affinity = None
        for line in tqdm(file, desc="Loading the graph"):
            if line.startswith("SRC"):
                source = line.split(":")[1].strip()
            elif line.startswith("TGT"):
                target = line.split(":")[1].strip()
            elif line.startswith("RES"):
                res = line.split(":")[1].strip()
                if res == "-1":
                    affinity = "-"
                else:
                    affinity = "+"
                graph.add_edge(source, target, affinity=affinity)
    return convert_to_undirected(graph)



'''
Function load_epinions_slash is used for loading graphs epinions and slashdot form textual files.
We can use the same function because the structure of textual files are the same.
'''



def load_epinions_slash(path):
    graph = nx.DiGraph()
    with open(path, "r") as file:
        for line in tqdm(file, desc="Loading the graph"):
            if line.startswith("#"):
                continue
            row = line.split("\t")
            affinity = None
            if "-1" in row[2]:
                affinity = "-"
            else:
                affinity = "+"
            graph.add_edge(row[0].strip(), row[1].strip(), affinity=affinity)
    return convert_to_undirected(graph)



'''
Function generate_random_graph is used for generation of a graph. We can adjust number of nodes, number of clusters,
chance of linking between two nodes and boolean value clusterable that represents is the graph clusterable or not.

If boolean clusterable is False, generated graph will have at least one negative edge in one cluster
'''



def generate_random_graph(number_of_nodes, number_of_clusters=1, chance_of_linking=0.5,clusterable = True):
    graph = nx.Graph()
    for i in tqdm(range(number_of_nodes), desc="Adding nodes to the graph"):
        cluster = random.randint(1, number_of_clusters)
        graph.add_node(i, cluster=cluster)


    for node in tqdm(graph.nodes, desc="Linking nodes"):
        for second_node in graph.nodes:
            if node == second_node:
                continue
            is_neighbor = random.random() > chance_of_linking

            if is_neighbor and not graph.has_edge(node, second_node):
                if graph.nodes[node]['cluster'] == graph.nodes[second_node]['cluster']:
                    graph.add_edge(node, second_node, affinity="+")

                else:
                    graph.add_edge(node, second_node, affinity="-")
    
    if not clusterable:

        changed = False
        for node in graph.nodes:
            for second_node in graph.nodes:
                if node == second_node:
                    continue
                
                if graph.has_edge(node,second_node) and graph.get_edge_data(node,second_node)['affinity'] == "+":
                    if not changed:
                        graph.edges[node,second_node]['affinity'] = "-"
                        changed = True
                    else:
                        change = random.random()>0.90
                        if change:
                            graph.edges[node,second_node]['affinity'] = "-"
                
    
    return graph


