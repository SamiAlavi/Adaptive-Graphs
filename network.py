from typing import List
from graph import Graph
import networkx as nx
import matplotlib.pyplot as plt

class Network(Graph):
    def __init__(self) -> None:
        super().__init__()

    def addGraphNodes(self) -> None:
        self.graph.add_nodes_from(self.nodes)

    def addGraphEdges(self) -> None:
        numNodes = len(self.nodes)
        for nodeAIndex in range(numNodes):
            nodeA = self.nodes[nodeAIndex]
            for nodeBIndex in range(numNodes):
                nodeB = self.nodes[nodeBIndex]
                weights = self.matrix[nodeAIndex][nodeBIndex]
                for weight in weights:
                    self.graph.add_edge(nodeA, nodeB, weight=weight)

    def printGraphProperties(self) -> None:
        print("Total number of nodes: ", int(self.graph.number_of_nodes()))
        print("Total number of edges: ", int(self.graph.number_of_edges()))
        print("Degree for all nodes: ", dict(self.graph.degree()))

    def drawGraph(self) -> None:
        seed = 13648  # Seed random number generators for reproducibility
        pos = nx.spring_layout(self.graph, seed=seed)
        plt.figure("Graph", figsize=(12,7))
        nx.draw(self.graph, pos, edge_color='black', width=1, linewidths=1, alpha=0.9, with_labels=True)
        edgeLabels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edgeLabels, font_color='red', font_family="arial")
        plt.axis('off')
        plt.show()
        

    def createGraph(self) -> None:
        self.graph = nx.DiGraph()

        self.addGraphNodes()
        self.addGraphEdges()
        self.printGraphProperties()


if (__name__ == "__main__"):
    network = Network()
    network.createGraph()
    network.drawGraph()

