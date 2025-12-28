import heapq
import networkx as nx
import matplotlib.pyplot as plt

def deijkstra(graph, start):
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    predecessors = {v: None for v in graph}
    
    heap = [(0, start)]  # бінарна купа: (відстань, вершина)
    visited = set()
    
    while heap:
        dist, u = heapq.heappop(heap)  # O(log V)
        
        if u in visited:
            continue
        visited.add(u)
        
        for v, weight in graph[u]:
            if v not in visited and dist + weight < distances[v]:
                distances[v] = dist + weight
                predecessors[v] = u
                heapq.heappush(heap, (distances[v], v))  # O(log V)
    
    return distances, predecessors

def get_path(predecessors, start, end):
    path, current = [], end
    while current:
        path.append(current)
        current = predecessors[current]
    return path[::-1] if path and path[-1] == start else []

def visualize_shortest(graph, distances, predecessors, start):
    G = nx.Graph()
    for u in graph:
        for v, w in graph[u]:
            if not G.has_edge(u, v):
                G.add_edge(u, v, weight=w)
    
    path_edges = {(predecessors[v], v) for v in predecessors if predecessors[v]}
    
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=2)
    nx.draw_networkx_edges(G, pos, 
        edgelist=[(u, v) for u, v in G.edges() if (u, v) in path_edges or (v, u) in path_edges],
        edge_color='red', width=3)
    
    colors = ['lightgreen' if v == start else 'lightblue' for v in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=700, edgecolors='black')
    
    labels = {v: f"{v}\n({distances[v]})" for v in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'))
    
    plt.title(f"Найкоротші шляхи від '{start}' (алгоритм Дейкстри)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('deijkstra_graph.png', dpi=150)
    plt.close()

def main():
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5), ('F', 12)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
        'E': [('C', 10), ('D', 2), ('F', 3)],
        'F': [('B', 12), ('D', 6), ('E', 3)],
    }

    start = 'A'
    distances, predecessors = deijkstra(graph, start)

    print("Найкоротші шляхи від вершини 'A':")
    print("-" * 40)
    for v in sorted(graph):
        path = get_path(predecessors, start, v)
        print(f"{v}: відстань = {distances[v]}, шлях: {' → '.join(path)}")

    visualize_shortest(graph, distances, predecessors, start)
    print("\nГраф збережено: deijkstra_graph.png")

if __name__ == "__main__":
    raise SystemExit(main())