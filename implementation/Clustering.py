import networkx as nx
from tqdm import tqdm


'''
function identify components is used for creating sets of nodes that represent clusters in graph
Bfs is modified so that we ignore neighbors with negative affinity and add positive neighbors dictionary of edges of current node
return value will be a tuple where the first element is a frozen set of nodes that represent clusters and dictionary of positive links between nodes
'''



def identify_components(graph: nx.Graph):
    visited = set()
    components = set()
    links = dict()
    for node in tqdm(graph.nodes, desc="identifying components of given graph"):
        if node not in visited:
            components.add(bfs(node, visited, graph,links))
    return frozenset(components), links



def bfs(start, visited, graph: nx.Graph,links):
    queue = list()
    comps = set()
    queue.append(start)
    visited.add(start)
    comps.add(start)
    while len(queue) != 0:
        current = queue.pop(0)
        neighbors = list(nx.neighbors(graph, current))
        tmp = {current:[]}
        for neighbor in neighbors[:]:
            if graph.get_edge_data(current, neighbor)['affinity'] == "-":
                neighbors.remove(neighbor)
        for neighbor in neighbors:
            tmp[current].append(neighbor)
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                comps.add(neighbor)
        links.update(tmp)
    return frozenset(comps)



'''
Function create_set_of_clusters takes clusters and links previously created in identify_components and our graph,
and returns a frozen set of all clusters that are represented as graphs. First we add all nodes from each set from clusters,
then we add edges that are in the dictionary of neighbors. This method is faster than copying the whole graph and then removing nodes
that are not in the cluster and faster than checking does the graph has edge between every two nodes in one cluster.
'''



def create_set_of_clusters(clusters,links, graph:nx.Graph):
    cluster_set = set()
    for cluster in tqdm(clusters,desc="Creating a set of clusters"):
        c_graph = nx.Graph()
        for node in cluster:
            c_graph.add_node(node)
            for n in links[node]:
                c_graph.add_edge(node,n,affinity="+")
        
        for node in c_graph.nodes:
            for second_node in c_graph.nodes:
                if node == second_node:
                    continue
                if graph.has_edge(node,second_node) and graph.get_edge_data(node, second_node)['affinity'] == "-":
                    c_graph.add_edge(node,second_node,affinity="-")

        cluster_set.add(c_graph)
    return frozenset(cluster_set)



'''
Function is_clusterable check if a graph is clusterable. Graph is clusterable if all edges in one cluster have positive affinity, and all edges
with negative affinity are edges between two clusters. If the graph has at least one negative edge in one of its clusters, graph is not clusterable.
In this function we can ignore (put them in coalitions without additional checking) cluster that have less than 3 nodes because they will always have
positive affinity.
'''



def is_clusterable(clusters):
    coalitions = set()
    anticoalitions = set()
    negative_links = list()

    for cluster in tqdm(clusters,desc="Checking graph clusterabillity"):
        if len(cluster.nodes)<3:
            coalitions.add(cluster)
        else:
            negative = [(u,v) for u, v, d in cluster.edges(data = True) if d['affinity'] == '-']
            if len(negative) == 0:
                coalitions.add(cluster)
                negative_links.extend(negative)
            else:
                anticoalitions.add(cluster)
                for i in negative:
                    if (i[1],i[0]) not in negative_links:
                        negative_links.append(i)
    
    if(len(anticoalitions)!=0):
        print("This graph is not clusterable")
        ans = input("Do you want to see what edges need to be deleted so the graph becomes clusterable (Y/N):")
        if ans == "y" or ans == "Y":
            for i in negative_links:
                print(i)
    else:
        print("This graph is clusterable")
    
    return coalitions,anticoalitions



'''
Function create_graph_of_cluster take our clusters and our graph and creates a new graph where each node represent one of our clusters.
Two nodes are connected if there is a connection between two clusters.
'''




def create_graph_of_clusters(clusters, graph: nx.Graph):
    graph_of_clusters = nx.Graph()
    cnt = 1

    for cluster in clusters:
        cluster.graph['name'] = str(cnt)
        cnt += 1
        graph_of_clusters.add_node(cluster)

    for cluster in tqdm(clusters,desc="Creating a graph of clusters"):
        for second_cluster in tqdm(clusters,leave=False):
            if cluster == second_cluster:
                continue

            connected = False
            cnt = 1

            while not connected and cnt < len(cluster.nodes):
                node = list(cluster.nodes)[cnt]
                cnt+=1
                for second_node in list(second_cluster.nodes):
                    if graph.has_edge(node,second_node):
                        connected = True
            if connected:
                graph_of_clusters.add_edge(cluster, second_cluster, affinity="-")
    return graph_of_clusters



'''
Function find_giant_component is used to find the component that have the largest amount of nodes in the graph
'''


def find_giant_component(clusters):
    m = 0
    giant = None
    for cluster in clusters:
        if len(cluster.nodes) > m:
            m = len(cluster.nodes)
            giant = cluster
    
    return giant