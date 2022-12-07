from typing import List
from typing import List
import numpy as np
import networkx as nx
from networkx import Graph

class Parser():
    def __init__(self) -> None:
        pass

    @staticmethod
    def bytes_to_string(bytes: bytes):
        return bytes.decode()

    @staticmethod
    def networkx_labels_to_matrix(nodes: List[str], labels: object) -> List[List[List[str]]]:
        num_nodes = len(nodes)
        matrix: List[List[List[str]]] = np.empty((num_nodes, num_nodes, 0), dtype=str).tolist()

        for (node_A, node_B), label in labels.items():
            try:
                node_A_index = nodes.index(node_A)
                node_B_index = nodes.index(node_B)
            except:
                node_A_index = int(node_A)
                node_B_index = int(node_B)
            try:
                matrix[node_A_index][node_B_index].append(label)
            except:
                matrix[node_A_index][node_B_index] = [label]

        return matrix

    @staticmethod
    def create_object(nodes: List[str], edges: List[str], matrix: List[List[List[str]]]) -> dict:
        return {
            "nodes": nodes,
            "matrix": matrix
        }

    @staticmethod
    def get_graph_nodes(graph: Graph, key="label") -> List[str]:
        nodes = []
        for _id, attributes in graph._node.items():
            try:
                nodes.append(attributes[key])
            except:
                nodes.append(_id)
        return nodes

    @staticmethod
    def get_edges_labels(graph: Graph, key="label") -> List[str]:
        return nx.get_edge_attributes(graph, key)

    @staticmethod
    def parse_gml(gml: bytes) -> dict:
        gml_str = Parser.bytes_to_string(gml)
        del(gml)
        graph = nx.parse_gml(gml_str)
        nodes = Parser.get_graph_nodes(graph)
        edges = list(graph.edges)
        edge_labels = Parser.get_edges_labels(graph, key='label')
        matrix = Parser.networkx_labels_to_matrix(nodes, edge_labels)
        return Parser.create_object(nodes, edges, matrix)

    @staticmethod
    def parse_graphml(graphml: bytes) -> dict:
        graphml_str = Parser.bytes_to_string(graphml)
        del(graphml)
        graph = nx.parse_graphml(graphml_str)
        nodes = Parser.get_graph_nodes(graph)
        edges = list(graph.edges)
        edge_labels = Parser.get_edges_labels(graph, key='LinkLabel')
        matrix = Parser.networkx_labels_to_matrix(nodes, edge_labels)
        return Parser.create_object(nodes, edges, matrix)
    