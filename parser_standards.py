from typing import List, Any, Callable
import numpy as np
from pathlib import Path
import json
import networkx as nx
from networkx import DiGraph, Graph, MultiDiGraph, MultiGraph

class Parser():
    def __init__(self) -> None:
        pass

    @staticmethod
    def bytes_to_string(bytes: bytes):
        return bytes.decode()

    @staticmethod
    def networkx_labels_to_matrix(nodes: List[str], labels: dict) -> List[List[List[str]]]:
        num_nodes = len(nodes)
        matrix: List[List[List[str]]] = np.empty((num_nodes, num_nodes, 0), dtype=str).tolist()

        for (node_A, node_B), label in labels.items():
            try:
                node_A_index = nodes.index(node_A)
                node_B_index = nodes.index(node_B)
            except:
                node_A = ''.join(filter(str.isdigit, node_A))
                node_B = ''.join(filter(str.isdigit, node_B))
                node_A_index = int(node_A)
                node_B_index = int(node_B)
            try:
                matrix[node_A_index][node_B_index].append(label)
            except:
                matrix[node_A_index][node_B_index] = [label]

        return matrix

    @staticmethod
    def parse_bytes(standard_bytes: bytes, parser: Callable[[str], (Any | DiGraph | Graph | MultiDiGraph | MultiGraph)], label_key: str) -> dict:
        standard_str = Parser.bytes_to_string(standard_bytes)
        del(standard_bytes)
        graph = parser(standard_str)
        nodes = Parser.get_graph_nodes(graph)
        edges = list(graph.edges)
        edge_labels = Parser.get_edges_labels(graph, key=label_key)
        matrix = Parser.networkx_labels_to_matrix(nodes, edge_labels)
        return Parser.get_json(nodes, edges, matrix)

    @staticmethod
    def get_json(nodes: List[str], edges: List[str], matrix: List[List[List[str]]]) -> dict:
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
    def get_edges_labels(graph: Graph, key) -> List[str]:
        return nx.get_edge_attributes(graph, key)

    @staticmethod
    def parse_gml(gml: bytes) -> dict:
        return Parser.parse_bytes(gml, nx.parse_gml, "label")

    @staticmethod
    def parse_graphml(graphml: bytes) -> dict:
        return Parser.parse_bytes(graphml, nx.parse_graphml, "label")

    @staticmethod
    def parse_json(json_bytes: bytes) -> dict:
        standard_str = Parser.bytes_to_string(json_bytes)
        del(json_bytes)
        obj = json.loads(standard_str)

        if (not ("nodes" in obj and "matrix" in obj)):
            return f'Request body JSON should have "nodes" and "matrix"'

        nodes = obj["nodes"]
        matrix = obj["matrix"]
        num_nodes = len(nodes)
        rows_matrix = len(matrix)

        if (rows_matrix < num_nodes):            
            return f"Matrix shape is not correct. Minimum required: ({num_nodes}, {num_nodes})"
        for row in matrix:
            if (len(row) < num_nodes):
                return f"Matrix shape is not correct. Minimum required: ({num_nodes}, {num_nodes})"
        return obj

    @staticmethod
    def parse(file: Any) -> dict:
        file_extension = Path(file.filename).suffix.lower()
        file.stream.seek(0)
        standard_bytes = file.read()
        if (file_extension == ".gml"):
            return Parser.parse_gml(standard_bytes)
        elif (file_extension == ".graphml"):
            return Parser.parse_graphml(standard_bytes)
        elif (file_extension == ".json"):
            return Parser.parse_json(standard_bytes)
        else:
            raise Exception(f"Extension not supported for parsing: '{file_extension}'")
    