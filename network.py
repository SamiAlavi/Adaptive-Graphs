import json
from typing import List
import networkx as nx
import matplotlib.pyplot as plt

class Network:
    jsonPath = "network generation/network.json"

    def readNetworkJson(self) -> dict:
        with open(self.jsonPath, 'r') as file:
            network = json.load(file)
            
        self.nodes = network["nodes"]
        self.matrix = network["matrix"]

    def __addGraphNodes(self):
        self.graph.add_nodes_from(self.nodes)

    def __addGraphEdges(self):
        numNodes = len(self.nodes)
        for nodeAIndex in range(numNodes):
            nodeA = self.nodes[nodeAIndex]
            for nodeBIndex in range(numNodes):
                nodeB = self.nodes[nodeBIndex]
                weights = self.matrix[nodeAIndex][nodeBIndex]
                for weight in weights:
                    self.graph.add_edge(nodeA, nodeB, weight=weight)

    def __printGraphProperties(self):
        print("Total number of nodes: ", int(self.graph.number_of_nodes()))
        print("Total number of edges: ", int(self.graph.number_of_edges()))
        print("Degree for all nodes: ", dict(self.graph.degree()))

    def drawGraph(self):
        seed = 13648  # Seed random number generators for reproducibility
        pos = nx.spring_layout(self.graph, seed=seed)
        plt.figure("Graph", figsize=(12,7))
        nx.draw(self.graph, pos, edge_color='black', width=1, linewidths=1, alpha=0.9, with_labels=True)
        edgeLabels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edgeLabels, font_color='red', font_family="arial")
        plt.axis('off')
        plt.show()
        

    def createGraph(self):
        self.graph = nx.DiGraph()

        self.__addGraphNodes()
        self.__addGraphEdges()
        self.__printGraphProperties()


if (__name__ == "__main__"):
    network = Network()
    network.readNetworkJson()
    network.createGraph()
    network.drawGraph()

