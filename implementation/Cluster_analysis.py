import networkx as nx
import math
from networkx.algorithms import cluster

from networkx.algorithms.shortest_paths.generic import average_shortest_path_length



'''
Sigmoid function is used for squashing the input in range from 0 to 1
'''



def sigmoid(x):
    return float(1/(1+math.exp(-x)))



'''
Function analysis is used for analysis of metrics scores for clusters
'''



def analysis(coalitions, anti_coalitions):
    length_of_coalitions = len(coalitions)
    length_of_anti_coalitions = len(anti_coalitions)

    coalitions_exist = length_of_coalitions > 0
    anti_coalitions_exist = length_of_anti_coalitions > 0

    metrics_of_coalitions = None
    metrics_of_anti_coalitions = None

    average_degree_score_of_coalitions = None
    average_degree_score_of_anti_coalitions = None

    density_score_of_coalitions = None
    density_score_of_anti_coalitions = None

    if coalitions_exist:
        metrics_of_coalitions = calculate_metrics_of_clusters(coalitions)
        average_degree_score_of_coalitions = calculate_score_of_metric(metrics_of_coalitions['average_degree'],length_of_coalitions)
        density_score_of_coalitions = calculate_score_of_metric(metrics_of_coalitions['density'],length_of_coalitions)

    if anti_coalitions_exist:
        metrics_of_anti_coalitions = calculate_metrics_of_clusters(anti_coalitions)
        average_degree_score_of_anti_coalitions = calculate_score_of_metric(metrics_of_anti_coalitions['average_degree'],length_of_anti_coalitions)
        density_score_of_anti_coalitions = calculate_score_of_metric(metrics_of_anti_coalitions['density'],length_of_anti_coalitions)

    if coalitions_exist and anti_coalitions_exist:
        if average_degree_score_of_coalitions > average_degree_score_of_anti_coalitions:
            print("Coalitions are more cohesive than anti coalitions")
        elif average_degree_score_of_coalitions < average_degree_score_of_anti_coalitions:
            print("Anti coalitions are more cohesive than coalitions")
        else:
            print("Coalitions and anti coalitions are equally cohesive")

        if density_score_of_coalitions > density_score_of_anti_coalitions:
            print("Coalitions are more dense than anti coalitions")
        
        elif density_score_of_coalitions < density_score_of_anti_coalitions:
            print("Anti coalitions are more dense than coalitions")

        else:
            print("Coalitions and anti coalitions are equally dense")




def calculate_metrics_of_clusters(cluster_set):
    metrics = {"average_degree":[],"density":[]}
    
    for cluster in cluster_set:
        metrics["average_degree"].append(average_degree(cluster))
        metrics["density"].append(density(cluster))

    return metrics



def calculate_score_of_metric(metric,cluster_length):
    return round(sigmoid(float(sum(metric)/cluster_length)),2)


def average_degree(cluster:nx.Graph):
    y = 0
    for node in cluster.nodes:
        y += cluster.degree(node)

    return float(y/len(cluster.nodes))



def density(cluster:nx.Graph):
    return float(len(cluster.edges)/(len(cluster.nodes)*(len(cluster.nodes))/2))



def diameter(cluster:nx.Graph):
    return nx.diameter(cluster)



def average_distance(cluster:nx.Graph):
    return nx.average_shortest_path_length(cluster)



def analyse_giant_component(graph:nx.Graph,giant_component:nx.Graph):
    print(f"Giant component has ~= {round(len(giant_component.nodes)/len(graph.nodes) * 100,2)}% of nodes in graph")
    print(f"Number of nodes: {len(giant_component.nodes)}")
    print(f"Number of edges: {len(giant_component.edges)}")
    print(f"Average degree: {average_degree(giant_component)}")
    print(f"Density: {density(giant_component)}")



def analyse_graph_of_clusters(graph_of_clusters:nx.Graph):
    print(f"Number of nodes: {len(graph_of_clusters.nodes)}")
    print(f"Number of edges: {len(graph_of_clusters.edges)}")
    print(f"Average degree: {average_degree(graph_of_clusters)}")
    print(f"Density: {density(graph_of_clusters)}")
    number_of_connected_components = nx.number_connected_components(graph_of_clusters)
    print(f"Number of connected components: {number_of_connected_components}")
    if number_of_connected_components > 1:
        print("Diameter, average distance: Could not calculate because there are more than 1 component")
    else:
        print(f"Diameter: {diameter(graph_of_clusters)}")
        print(f"Average distance: {average_distance(graph_of_clusters)}")
