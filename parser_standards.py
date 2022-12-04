import tempfile
from os import path, remove
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
    def write_to_temp_file(string_bytes: bytes) -> str:
        temp =  tempfile.NamedTemporaryFile(prefix='_ADG_', suffix='.adg', delete=False)
        temp.write(string_bytes)
        temp.seek(0)
        temp.close()
        return temp.name

    @staticmethod
    def remove_file(file_path: str) -> None:
        if (path.exists(file_path)):
            remove(file_path)

    @staticmethod
    def networkx_labels_to_matrix(nodes: List[str], labels: object) -> List[List[List[int]]]:
        num_nodes = len(nodes)
        matrix = np.zeros((num_nodes, num_nodes, 0), dtype=int).tolist()

        for (node_A, node_B), label in labels.items():
            node_A_index = nodes.index(node_A)
            node_B_index = nodes.index(node_B)
            label = int(label)
            try:
                matrix[node_A_index][node_B_index].append(label)
            except:
                matrix[node_A_index][node_B_index] = [label]

        return matrix

    @staticmethod
    def create_object(nodes: List[str], edges: List[str], matrix: List[List[List[int]]]) -> object:
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
    def parse_gml(gml: bytes) -> object:
        gml_str = Parser.bytes_to_string(gml)
        del(gml)
        graph = nx.parse_gml(gml_str)
        nodes = Parser.get_graph_nodes(graph)
        edges = list(graph.edges)
        labels = nx.get_edge_attributes(graph, 'label')
        matrix = Parser.networkx_labels_to_matrix(nodes, labels)
        return Parser.create_object(nodes, edges, matrix)

    @staticmethod
    def parse_graphml(graphml: bytes) -> object:
        graphml_str = Parser.bytes_to_string(graphml)
        del(graphml)
        graph = nx.parse_graphml(graphml_str)
        nodes = Parser.get_graph_nodes(graph)
        edges = list(graph.edges)
        labels = nx.get_edge_attributes(graph, 'label')
        matrix = Parser.networkx_labels_to_matrix(nodes, labels)
        return Parser.create_object(nodes, edges, matrix)
    