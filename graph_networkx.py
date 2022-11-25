import networkx as nx
import matplotlib.pyplot as plt
from graph_base import BaseGraph

class NetworkX(BaseGraph):
    def __init__(self) -> None:
        super().__init__()
        self.graph = nx.DiGraph()

    def add_graph_nodes(self) -> None:
        for node in super()._get_graph_nodes():
            self.graph.add_node(node)

    def add_graph_edges(self) -> None:
        for node_a, node_b, weight in super()._get_graph_edges():
            self.graph.add_edge(node_a, node_b, weight=weight)

    def print_graph_properties(self) -> None:
        print("Total number of nodes: ", int(self.graph.number_of_nodes()))
        print("Total number of edges: ", int(self.graph.number_of_edges()))
        print("Degree for all nodes: ", dict(self.graph.degree()))

    def draw_graph(self) -> None:
        seed = 13648  # Seed random number generators for reproducibility
        pos = nx.spring_layout(self.graph, seed=seed)
        plt.figure("Graph_NetworkX", figsize=(12,7))
        nx.draw(self.graph, pos, edge_color='black', width=1, linewidths=1, alpha=0.9, with_labels=True)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red', font_family="arial")
        plt.axis('off')
        plt.show()


if (__name__ == "__main__"):
    graph = NetworkX()
    graph.read_network_json()
    graph.create_graph()
    graph.draw_graph()
