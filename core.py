import networkx as nx
import matplotlib.pyplot as plt
import requests
import gzip
import shutil


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
        print(current)
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
