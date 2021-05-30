import networkx as nx



'''
Identify components is used for detecting clusters in given graphs. It uses modified BFS for detecting. It is modified in a way that we ignore neighbors
which are connected with negative affinity link, after that we put each neighbor, that is not already visited, in a set of nodes that represents a cluster
'''



def identify_components(graph: nx.Graph):
    visited = set()
    components = set()
    print("Identifying components...")
    for node in graph.nodes:
        if node not in visited:
            components.add(bfs(node, visited, graph))
    print("Identified!")
    return frozenset(components)



def bfs(start, visited, graph: nx.Graph):
    queue = list()
    comps = set()
    queue.append(start)
    visited.add(start)
    comps.add(start)
    while len(queue) != 0:
        current = queue.pop(0)
        for neighbor in list(nx.neighbors(graph, current)):
            if graph.get_edge_data(current,neighbor)['affinity'] == "-":
                continue
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                comps.add(neighbor)
    return frozenset(comps)



'''
create_set_of_clusters is used to take nodes from each cluster represented as a frozen set, create a graph with those nodes, link every neighbor in that
cluster, and put them inside a set that will the return value. Graph representation of clusters is needed if we want to use functions is_clusterable,
create_network_of_clusters
'''



def create_set_of_clusters(clusters, graph:nx.Graph):
    print("Creating a set of clusters...")
    cluster_set = set()
    for cluster in clusters:
        cluster_graph = nx.Graph()
        if len(cluster) == 1:
            for n in cluster:
                cluster_graph.add_node(n)
        else:
            for node in cluster:
                for second_node in cluster:
                    if node == second_node:continue
                    if graph.has_edge(node,second_node) and not cluster_graph.has_edge(node,second_node):
                        cluster_graph.add_edge(node,second_node,affinity = graph.get_edge_data(node,second_node)['affinity'])
        cluster_set.add(cluster_graph)
    print("Created!")
    return frozenset(cluster_set)



'''
is_clusterable checks if the given graph is clusterable or not. It can return coalitions, anticoalitions and negative links inside clusters that need to be 
removed so the graph becomes clusterable. We can ignore clusters that have less than three nodes because those clusters definitley do not contain a negative
affinity edge.
'''



def is_clusterable(clusters):
    coalitions = set()
    anti_coalitions = set()
    negative_links = list()
    print("Checking if graph is clusterable...")
    for cluster in clusters:
        if len(cluster.nodes) < 3:
            coalitions.add(cluster)
            continue

        negative = [(u,v) for u, v, d in cluster.edges(data = True) if d['affinity'] == '-']
        if len(negative) == 0:
            coalitions.add(cluster)
        else:
            anti_coalitions.add(cluster)
            for i in negative:
                if (i[1],i[0]) not in negative_links:
                    negative_links.append(i)
    
    if len(anti_coalitions)!=0:
        print("This graph is not clusterable")
    else:
        print("This graph is clusterable")

    return coalitions, anti_coalitions, negative_links



'''
create_graph_of_cluster take our clusters and our graph and creates a new graph where each node represent one of our clusters.
Two nodes are connected if there is a connection between two clusters.
'''



def create_network_of_clusters(clusters,graph:nx.Graph):
    print("Creating a network of clusters...")
    new_graph = nx.Graph()
    counter = 1
    for cluster in clusters:
        cluster.graph['name'] = str(counter)
        counter += 1
        new_graph.add_node(cluster)
    

    visited_pairs = set()

    for cluster in clusters:
        for second_cluster in clusters:
            if cluster == second_cluster or (second_cluster,cluster) in visited_pairs:
                continue
            visited_pairs.add((cluster,second_cluster))
            connected = False
            for node in cluster:
                for second_node in second_cluster:
                    if graph.has_edge(node,second_node):
                        connected = True
                        new_graph.add_edge(cluster,second_cluster,affinity="-")
                        break
                if connected: break
    print("Created!")
    return new_graph



'''
find_giant_component is used for fiding giant component in our graph. If there is no giant component, this function will return None value
'''



def find_giant_component(clusters,graph:nx.Graph):
    graph_components = sorted(nx.connected_components(graph), key=len, reverse=True)
    giant = graph.subgraph(graph_components[0])
    return giant