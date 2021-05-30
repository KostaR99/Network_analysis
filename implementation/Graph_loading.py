import networkx as nx
import random


'''
Function convert_to_undirected is used to convert directed graph to undirected.
If there is at least one negative edges between two nodes, edge between those two nodes in undirected graph will have negative affinity 
'''



def convert_to_undirected(graph):
    undirected_graph = nx.Graph()
    undirected_graph.add_edges_from(graph.edges(), affinity="")
    for u, v in graph.edges():
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
Function for loading small hand-crafted graphs that are clusterable or unclusterable
'''



def load_small_graph(path):
    graph = nx.Graph()
    print("Loading a graph...")
    with open(path,'r') as file:
        for line in file:
            row = line.split(" ")
            graph.add_edge(row[0].strip(),row[1].strip(),affinity=row[2].strip())
    print("Loaded!")
    return graph



'''
Function load_wiki loads a wiki-RfA graph that is in form of a textual file
'''



def load_wiki(path):
    graph = nx.DiGraph()
    print("Loading the graph...")
    with open(path, "r", encoding="utf8") as file:
        for line in file:
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
    print("Loaded!")
    return convert_to_undirected(graph)



'''
Function load_epinions_slash is used for loading graphs epinions and slashdot form textual files.
We can use the same function because the structure of textual files are the same.
'''



def load_epinions_slash(path):
    graph = nx.DiGraph()
    print("Loading the graph...")
    with open(path, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            row = line.split("\t")
            affinity = None
            if "-1" in row[2]:
                affinity = "-"
            else:
                affinity = "+"
            graph.add_edge(row[0].strip(), row[1].strip(), affinity=affinity)
    print("Loaded!")
    return convert_to_undirected(graph)



'''
Function generate_random_graph is used for generation of a graph. We can adjust number of nodes, number of clusters,
chance of linking between two nodes and boolean value clusterable that represents is the graph clusterable or not.

If boolean clusterable is False, generated graph will have at least one negative edge in one cluster
'''



def generate_random_graph(number_of_nodes, number_of_clusters,clusterable = True):
    print("Generating random graph...")
    graph = nx.Graph()
    for i in range(number_of_nodes):
        cluster = random.randint(1, number_of_clusters)
        graph.add_node(i, cluster=cluster)

    bad_link = False

    for node in graph.nodes:
        for second_node in graph.nodes:
            if node == second_node:
                continue
            is_neighbor = random.uniform(0,1) > 0.05

            if is_neighbor and not graph.has_edge(node, second_node) and graph.degree[node] < 3 and graph.degree[second_node] < 3:
                if graph.nodes[node]['cluster'] == graph.nodes[second_node]['cluster']:
                    if not clusterable:
                        if not bad_link:
                            graph.add_edge(node, second_node, affinity="-")
                            bad_link = True
                        else:
                            chance = random.uniform(0,1) > 0.25
                            if chance:
                                graph.add_edge(node, second_node, affinity="-")
                            else:
                                graph.add_edge(node, second_node, affinity="+")

                    else:
                        graph.add_edge(node,second_node,affinity="+")

                else:
                    graph.add_edge(node, second_node, affinity="-")
    print("Generated!")   
    return graph