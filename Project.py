import networkx as nx
import time
from collections import defaultdict
import heapq

def readEdgesfromFile(filename):
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            u, v = map(int, line.strip().replace(',', ' ').split())
            edges.append((u,v))
    return edges
            
def createGraph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

import networkx as nx
from collections import Counter

def calculate_cpl(G):
    # Calculate CPL of a graph
    try:
        return nx.average_shortest_path_length(G)
    except:
        return 0

def edge_to_remove(G):
    # Find the edge to remove
    all_shortest_paths = nx.shortest_path(G)
    edges = []
    for source in all_shortest_paths:
        for target in all_shortest_paths[source]:
            edges += zip(all_shortest_paths[source][target][:-1], all_shortest_paths[source][target][1:])
    return Counter(edges).most_common(1)[0][0]

def process_graph(G):
    # Calculate CPL and print it
    print(f"CPL of the graph: {calculate_cpl(G)}")

    # Calculate CPL for each component and print it
    for component in nx.connected_components(G):
        subgraph = G.subgraph(component)
        print(f"CPL of component with nodes {len(component)}: {calculate_cpl(subgraph)}")

    # Find and print the component with the most nodes
    largest_component = max(nx.connected_components(G), key=len)
    print(f"Component with the most nodes ({len(largest_component)}): {largest_component}")

    # Stop if any component is a single node
    if any(len(component) == 1 for component in nx.connected_components(G)):
        return

    # Remove the edge with the most appearances in the shortest paths
    G.remove_edge(*edge_to_remove(G))

    # Recursively process each component
    for component in nx.connected_components(G):
        subgraph = G.subgraph(component).copy()
        process_graph(subgraph)


start_time = time.process_time()
filename = input("Please insert filename: ")
edges = readEdgesfromFile(filename)
Graph = createGraph(edges)
process_graph(Graph)
end_time = time.process_time()
elapsed_time = end_time - start_time
print(f"CPU execution time: {elapsed_time:.2f} seconds")
    


    
