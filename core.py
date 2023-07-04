import networkx as nx
import matplotlib.pyplot as plt
import requests
import gzip
import shutil
import heapq


def plot_graph(graph, figsize=(8, 6), arrows=False):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=figsize)

    edge_labels = nx.get_edge_attributes(graph, "weight")

    # Draw the graph
    nx.draw(
        graph,
        pos,
        with_labels=True,
        edge_color="gray",
        node_color="lightblue",
        arrows=arrows,
    )

    # Draw the edge labels
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=edge_labels, ax=ax, font_size=6
    )

    plt.show()


def dijkstra(graph, start):
    distances = {
        node: float("inf") for node in graph
    }  # Inicializa as distâncias como infinito para todos os vértices
    distances[start] = 0
    previous = {
        node: None for node in graph
    }  # Inicializa os vértices antecessores como "vazio"
    closed = set()  # Auxiliar para armazenar os visitados
    open_set = set(graph.keys())  # Auxiliar para armazenar os ainda não visitados

    while open_set:
        current = min(open_set, key=distances.get)
        open_set.remove(current)
        closed.add(current)

        for neighbor, weight in graph[current].items():
            if neighbor in closed:
                continue  # Pula os vizinhos que já foram visitados

            cost = (
                distances[current] + weight
            )  # Calcula o custo do início até o vizinho passando pelo vértice atual

            if cost < distances[neighbor]:
                distances[neighbor] = cost
                previous[neighbor] = current

    return distances, previous


def download_data(url, file_path):
    response = requests.get(url, stream=True)
    with open(file_path, "wb") as file:
        shutil.copyfileobj(response.raw, file)

    with gzip.open(file_path, "rb") as file:
        content = file.read()

    with open(file_path.replace(".gz", ""), "wb") as file:
        file.write(content)


def read_gr_graph(file_path):
    graph = nx.Graph()

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith(("c", "p")):
                continue
            if line.startswith("a"):
                _, source, target, weight = line.split()
                graph.add_edge(source, target, weight=float(weight))
    return graph


def prim(graph, start):
    minimum_spanning_tree = []  # Cria árvore vazia
    all_vertices = set(graph.keys())
    visited_vertices = {start}
    aux_heap = []
    total_weight = 0  # Custo total da árvore

    # Adicionas da fila os vizinhos do vertice inicial
    for neighbor, weight in graph[start].items():
        heapq.heappush(aux_heap, (weight, start, neighbor))

    while len(aux_heap) > 0 and len(visited_vertices) != len(all_vertices):
        weight, u, v = heapq.heappop(aux_heap)  # Pega e devolva o menor item da pilha

        # pula se já foi visitado
        if v in visited_vertices:
            continue

        minimum_spanning_tree.append((u, v, weight))
        total_weight += weight
        visited_vertices.add(v)

        # Adiciona arestas do vértice recém-visitado ao heap
        for neighbor, weight in graph[v].items():
            if neighbor not in visited_vertices:
                heapq.heappush(aux_heap, (weight, v, neighbor))

    return minimum_spanning_tree, total_weight

def kruskal(graph):
    edges = [(n1, n2, graph[n1][n2]) for n1 in graph.keys() for n2 in graph[n1]]
    edges_sorted = sorted(edges, key=lambda x: x[2])
    all_sets = {x: {x} for x in graph.keys()}
    n_graph = len(graph.keys()) - 1
    total_cost = 0
    minimum_spanning_tree = []

    for n1, n2, weight in edges_sorted:
        if all_sets[n1].isdisjoint(all_sets[n2]):
            values_in_set = all_sets[n1] | all_sets[n2]
            all_sets[n1] = values_in_set
            all_sets[n2] = values_in_set
            total_cost += weight
            minimum_spanning_tree.append((n1, n2, weight))
        if len(minimum_spanning_tree) == n_graph:
            break
    return minimum_spanning_tree, total_cost