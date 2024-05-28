import igraph as ig
import numpy as np
import heapq
import time


def process_graph(g, first_execution):
    # Υπολογισμός του CPL
    cpl = g.average_path_length()
    print(f'Initial CPL: {cpl}')

    # Υπολογισμός του συνολικού αριθμού των συντομοτέρων μονοπατιών (SPs)
    sp_counts = np.zeros(g.ecount())
    for v in range(g.vcount()):
        sps = g.get_all_shortest_paths(v)
        for sp in sps:
            for i in range(len(sp) - 1):
                e = g.get_eid(sp[i], sp[i+1])
                sp_counts[e] += 1
    edge_order = np.argsort(sp_counts)[::-1]

    # Αφαίρεση της ακμής στην κορυφή της διάταξης
    g.delete_edges(edge_order[0])
    edge_order = edge_order[1:]

    # Check if the graph is still connected
    if not g.is_connected():
        # If not, process each component separately
        if first_execution == True:
            
            components = g.components()
            subgraphs = [g.subgraph(vertices) for i, vertices in enumerate(components) if i != 0]
            for i, subgraph in enumerate(subgraphs):
                print(f"Subgraph {i+1}: {subgraph.summary()}")
            first_execution = False
        else:
            components = g.components()
            subgraphs = [g.subgraph(vertices) for vertices in components]
            for i, subgraph in enumerate(subgraphs):
                print(f"Subgraph {i+1}: {subgraph.summary()}")
            

        largest_subgraph = None
        smallest_subgraph = None
       
        # Iterate over the subgraphs
        for subgraph in subgraphs:
        # If this is the first subgraph, or it has more nodes than the current largest, update largest_subgraph
            if largest_subgraph is None or subgraph.vcount() > largest_subgraph.vcount():
                largest_subgraph = subgraph
        # If this is the first subgraph, or it has fewer nodes than the current smallest, update smallest_subgraph
            if smallest_subgraph is None or subgraph.vcount() < smallest_subgraph.vcount():
                smallest_subgraph = subgraph

        print(f"Largest component has a size of {largest_subgraph.vcount()}")
        print(f"Smallest component has a size of {smallest_subgraph.vcount()}")
        if smallest_subgraph.vcount() == 1:
            print("Single node found, exiting")
            return
        else:
            for i in range(len(subgraphs)):
                if subgraphs[i].vcount() > 1:
                    process_graph(subgraphs[i],first_execution)

    if g.is_connected():
        process_graph(g,first_execution)            

    


edges = []
filename = input("Please insert filename: ")
with open(filename, 'r') as file:
    for line in file:
        u, v = map(int, line.strip().replace(',', ' ').split())
        edges.append((u,v))
g = ig.Graph(edges, directed=False)


start_time = time.time()
first_execution = True
process_graph(g, first_execution)
end_time = time.time()
execution_time = end_time - start_time
print(f'Execution time: {execution_time} seconds')

    
