
import heapq
from collections import defaultdict

def dijkstra_with_path(graph, source, target, max_distance=float('inf')):
    # Initialize distances, predecessors, and priority queue
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    predecessor = {node: None for node in graph}
    priority_queue = [(0, source)]  # (distance, node)
    
    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)
        
        if current_node == target:
            break
        
        if current_dist > dist[current_node]:
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            if distance < dist[neighbor] and weight <= max_distance:
                dist[neighbor] = distance
                predecessor[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # Reconstruct the path from source to target
    path = []
    step = target
    while step:
        path.append(step)
        step = predecessor[step]
    
    path.reverse()
    
    return dist[target], path

# Graph representation with multiple edges from the provided image
graph = defaultdict(list)
graph['Thessaloniki'].extend([('A', 80), ('B', 110)])
graph['A'].extend([('Thessaloniki', 80), ('C', 60), ('B', 50)])
graph['B'].extend([('Thessaloniki', 110), ('A', 60),('C', 10),('D', 60)])
graph['C'].extend([('A', 60), ('B', 10), ('D',60), ('Athens', 100)])
graph['D'].extend([('B', 60), ('C', 60), ('Athens', 70)])
graph['Athens'].extend([('D', 70), ('C', 100)])

# Additional edges with different weights
graph['Thessaloniki'].extend([('A', 70)])
graph['D'].extend([('Athens', 60)])
graph['Athens'].extend([('D', 60)])
# For B: Shortest path with m = infinity
shortest_dist_inf, shortest_path_inf = dijkstra_with_path(graph, 'Thessaloniki', 'Athens')
print("Shortest path with m = infinity:", shortest_dist_inf)
print("Nodes of the shortest path with m = infinity:", shortest_path_inf)

# For C: Shortest path with m = 100
shortest_dist_100, shortest_path_100 = dijkstra_with_path(graph, 'Thessaloniki', 'Athens', max_distance=100)
print("Shortest path with m = 100:", shortest_dist_100)
print("Nodes of the shortest path with m = 100:", shortest_path_100)