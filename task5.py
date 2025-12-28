import uuid

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


class Node:
  def __init__(self, key, color="skyblue"):
    self.left = None
    self.right = None
    self.val = key
    self.color = color # Додатковий аргумент для зберігання кольору вузла
    self.id = str(uuid.uuid4()) # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
  if node is not None:
    graph.add_node(node.id, color=node.color, label=node.val) # Використання id та збереження значення вузла
    if node.left:
      graph.add_edge(node.id, node.left.id)
      l = x - 1 / 2 ** layer
      pos[node.left.id] = (l, y - 1)
      l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
    if node.right:
      graph.add_edge(node.id, node.right.id)
      r = x + 1 / 2 ** layer
      pos[node.right.id] = (r, y - 1)
      r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
  return graph


def draw_tree(tree_root):
  tree = nx.DiGraph()
  pos = {tree_root.id: (0, 0)}
  tree = add_edges(tree, tree_root, pos)

  colors = [node[1]['color'] for node in tree.nodes(data=True)]
  labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)} # Використовуйте значення вузла для міток

  plt.figure(figsize=(8, 5))
  nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
  plt.show()

def heap_to_tree(heap):
    if not heap:
        return None
    
    nodes = [Node(val) for val in heap]
    for i in range(len(nodes)):
        if 2 * i + 1 < len(nodes):
            nodes[i].left = nodes[2 * i + 1]
        if 2 * i + 2 < len(nodes):
            nodes[i].right = nodes[2 * i + 2]
    return nodes[0]

#Градієнт кольорів від темного до світлого
def generate_gradient_colors(n, base_color=(18, 150, 240)):
    colors = []
    
    for i in range(n):
        # Коефіцієнт від 0.3 (темний) до 1.0 (світлий)
        factor = 0.3 + (0.7 * i / max(n - 1, 1))
    
        r = int(base_color[0] + (255 - base_color[0]) * factor)
        g = int(base_color[1] + (255 - base_color[1]) * factor)
        b = int(base_color[2] + (255 - base_color[2]) * factor)
    
        colors.append(f'#{r:02X}{g:02X}{b:02X}')
    
    return colors

# Обхід у глибину (DFS) з використанням стеку
def dfs_traversal(root):
    if not root:
        return []
    
    visited_order = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        visited_order.append(node)
        
        # Додаємо правий вузол першим, щоб лівий оброблявся раніше
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return visited_order

# Обхід у ширину (BFS) з використанням черги
def bfs_traversal(root):
    if not root:
        return []
    
    visited_order = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        visited_order.append(node)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return visited_order

# Візуалізація обходу дерева з градієнтом кольорів
def visualize_traversal(root, traversal_func, title="Tree Traversal"):
    if not root:
        return
    
    # Отримуємо порядок обходу
    visited_order = traversal_func(root)
    n = len(visited_order)
    
    # Генеруємо градієнт кольорів
    colors = generate_gradient_colors(n)
    
    # Присвоюємо кольори вузлам відповідно до порядку обходу
    node_colors = {}
    for i, node in enumerate(visited_order):
        node_colors[node.id] = colors[i]
    
    # Будуємо граф
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    
    def add_edges_with_colors(graph, node, pos, x=0, y=0, layer=1):
        if node is not None:
            graph.add_node(node.id, color=node_colors.get(node.id, "skyblue"), label=node.val)
            if node.left:
                graph.add_edge(node.id, node.left.id)
                l = x - 1 / 2 ** layer
                pos[node.left.id] = (l, y - 1)
                add_edges_with_colors(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
            if node.right:
                graph.add_edge(node.id, node.right.id)
                r = x + 1 / 2 ** layer
                pos[node.right.id] = (r, y - 1)
                add_edges_with_colors(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
        return graph
    
    tree = add_edges_with_colors(tree, root, pos)
    
    # Отримуємо кольори та мітки для візуалізації
    node_color_list = [tree.nodes[node_id]['color'] for node_id in tree.nodes()]
    labels = {node_id: tree.nodes[node_id]['label'] for node_id in tree.nodes()}
    
    # Візуалізація
    plt.figure(figsize=(10, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, 
            node_color=node_color_list, font_size=10, font_weight='bold')
    plt.title(title, fontsize=14, fontweight='bold')
    
    # Додаємо легенду з порядком обходу
    order_text = " → ".join([str(node.val) for node in visited_order])
    plt.figtext(0.5, 0.02, f"Порядок обходу: {order_text}", ha='center', fontsize=10)
    
    plt.subplots_adjust(bottom=0.15)
    plt.show()

def visualize_dfs(root):
    visualize_traversal(root, dfs_traversal, "Обхід у глибину (DFS) - використано стек")


def visualize_bfs(root):
    visualize_traversal(root, bfs_traversal, "Обхід у ширину (BFS) - використано чергу")


def main():
    heap = [100, 19, 36, 17, 3, 25, 1, 2, 7]
    heap_root = heap_to_tree(heap)
    
    print("Оригінальне дерево:")
    draw_tree(heap_root)
    
    print("\nВізуалізація DFS:")
    visualize_dfs(heap_root)
    
    print("\nВізуалізація BFS:")
    visualize_bfs(heap_root)

if __name__ == "__main__":
    raise SystemExit(main())
