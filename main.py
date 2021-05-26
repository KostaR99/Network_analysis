from implementation.Graph_loading import load_epinions_slash, load_wiki,generate_random_graph, load_small_graph
from implementation import Clustering
from implementation.Cluster_analysis import analysis, analyse_graph_of_clusters, analyse_giant_component
import networkx as nx

'''
Subject for change
'''

def load_graph():
    print("Choose what graph you want to load:")
    choice = int(input("1) Wiki-RfA\n2)Epinions\n3)Slashdot\n4)Random graph\n5)Small graph\n->"))
    graph = None
    if choice == 1:
        graph = load_wiki("D:\graph_clusterability\data\wiki-RfA.txt")
    elif choice == 2:
        graph = load_epinions_slash("D:\graph_clusterability\data\epinions.txt")
    elif choice == 3:
        graph = load_epinions_slash("D:\graph_clusterability\data\slashdot.txt")
    elif choice == 4:
        graph = generate_random_graph(1000,100,clusterable=False)
    elif choice == 5:
        graph = load_small_graph()
    return graph

def is_graph_clusterable(graph:nx.Graph):
    clusters = Clustering.identify_components(graph)
    print("Number of clusters in the graph is: "+str(len(clusters[0])))
    cluster_g = Clustering.create_set_of_clusters(clusters[0],clusters[1],graph)
    coalitions, anticoalitions = Clustering.is_clusterable(cluster_g)
    print("Number of coalitions: "+str(len(coalitions)))
    print("Number of anti coalitions: "+str(len(anticoalitions)))
    analysis(coalitions,anticoalitions)

    giant = Clustering.find_giant_component(cluster_g)
    print("\nStructure of giant component:\n")
    analyse_giant_component(graph,giant)
    graph_of_clusters = Clustering.create_graph_of_clusters(cluster_g,graph)
    print("\nStructure of graph of clusters:\n")
    analyse_graph_of_clusters(graph_of_clusters)
if __name__ == '__main__':
    graph = load_graph()
    is_graph_clusterable(graph)

