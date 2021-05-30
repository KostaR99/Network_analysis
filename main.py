from implementation.Graph_loading import load_epinions_slash, load_wiki,generate_random_graph, load_small_graph
from implementation import Clustering
from implementation import Cluster_analysis
import networkx as nx
import os
import sys
'''
Subject for change
'''

def load_graph():
    graph = None
    while graph == None:
        print("Choose what graph you want to load:")
        choice = input("1) Wiki-RfA\n2)Epinions\n3)Slashdot\n4)Random graph\n5)Small graph\n->")
        if choice == "1":
            graph = load_wiki("D:\graph_clusterability\data\wiki-RfA.txt")
        elif choice == "2":
            graph = load_epinions_slash("D:\graph_clusterability\data\epinions.txt")
        elif choice == "3":
            graph = load_epinions_slash("D:\graph_clusterability\data\slashdot.txt")
        elif choice == "4":
            number_of_nodes = int(input("Input number of nodes you want to have in the graph: "))
            number_of_clusters = int(input("Input number of nodes you want to have in the graph: "))
            clusterable = input("Do you want this graph to be clusterable (Y/N): ")
            if clusterable == "y" or clusterable == "Y":
                clusterable = True
            else:
                clusterable = False
            graph = generate_random_graph(number_of_nodes,number_of_clusters,clusterable=clusterable)
        elif choice == "5":
            graph_choice = input("What graph do you want to load:\n1) Clusterable\n2) Unclusterable\n->")
            if graph_choice == "1":
                graph = load_small_graph("D:\graph_clusterability\data\small_clusterable_graph.txt")
            elif graph_choice == "2":
                graph = load_small_graph("D:\graph_clusterability\data\small_unclusterable_graph.txt")
        os.system("cls") #for windows, for unix systems it is 'os.system("clear")'
    return graph
            

    
        
            


def graph_analysis(graph:nx.Graph):
    print("Results of graph analysis: \n")
    clusters = Clustering.identify_components(graph)
    print(f"Number of clusters: {len(clusters)}\n")
    set_of_clusters = Clustering.create_set_of_clusters(clusters,graph)
    triplet_set = Clustering.is_clusterable(set_of_clusters)
    print(f"Number of coalitions: {len(triplet_set[0])}")
    print(f"Number of anti coalitions: {len(triplet_set[1])}")
    print(f"Number of links that violate clusterabillity: {len(triplet_set[2])}")
    if len(triplet_set[2]) != 0:
        answer = input("Do you want to print edges that need to be removed so the graph becomes clusterable (Y/ any other key): ")
        if answer == "y" or answer == "Y":
            print("Edges that need to be removed so the graph becomes clusterable: ")
            for i in triplet_set[2]:
                print(i)
            print("\n")

    Cluster_analysis.analysis(triplet_set[0],triplet_set[1])
    giant_component = Clustering.find_giant_component(set_of_clusters,graph)

    print("\n")
    Cluster_analysis.analyse_giant_component(graph,giant_component)
    print("\n")
    
    network_of_clusters = Clustering.create_network_of_clusters(set_of_clusters,graph)

    Cluster_analysis.analyse_graph_of_clusters(network_of_clusters)

            


if __name__ == '__main__':
    graph = load_graph()
    graph_analysis(graph)