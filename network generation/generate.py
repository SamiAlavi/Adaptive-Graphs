from typing import Generator, List, Tuple
from string import ascii_uppercase
import json
import numpy as np
from jsonschema import validate
import os

def check_directory():
    folder_name = "network generation"
    if (folder_name in os.listdir()):
        os.chdir(folder_name)

def column_to_excel(col) -> str: # col is 1 based
    excel_col = str()
    div = col
    while div:
        (div, mod) = divmod(div-1, 26) # will return (x, 0 .. 25)
        excel_col = ascii_uppercase[mod] + excel_col

    return excel_col

def generate_column_names(num_columns: int) -> List[str]:
    titles = list(ascii_uppercase)

    if (num_columns <= 26):
        return titles[:num_columns]

    num_columns-=26
    times = 0

    while (num_columns > 0):
        sublist = [titles[times]+char for char in ascii_uppercase][:num_columns]
        titles.extend(sublist)
        num_columns-=26
        times+=1

    return titles

def generate_matrix(num_nodes: int, max_connections_between_nodes: int) -> List[List[List[str]]]:
    matrix = np.random.randint(0, 10, (num_nodes, num_nodes, max_connections_between_nodes)).astype(str)
    matrix[matrix=='0'] = ''
    return matrix.tolist()

def write_json(nodes: List[str], matrix: List[List[List[str]]], minify_json: bool) -> None:
    data = {
        'nodes': nodes,
        'matrix': matrix
    }
    indent = None if minify_json else 4

    with open("network.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=indent)

def get_graph_edges(nodes: List[str], matrix: List[List[List[str]]]) -> Generator[Tuple[str, str, str], None, None]:
    num_nodes = len(nodes)
    for node_a_index in range(num_nodes):
        node_a = nodes[node_a_index]
        for node_b_index in range(num_nodes):
            node_b = nodes[node_b_index]
            labels = matrix[node_a_index][node_b_index]
            for label in labels:
                if (label != ''):
                    yield node_a, node_b, label

def create_graphjson(nodes: List[str], matrix: List[List[List[str]]], minify_json: bool) -> None:
    graph_json = {
        "graph": {
            "directed": True,
            "type": "graph type",
            "label": "graph label",
            "metadata": {
                "user-defined": "values"
            },
            "nodes": {},
            "edges": []
        }
    }
    for node in nodes:
        graph_json["graph"]["nodes"][node] = {
            "label": f"{node}",
            "metadata": {
                "type": "node type",
            }
        }
    for node_a, node_b, label in get_graph_edges(nodes, matrix):
        edge = {
            "source": f"{node_a}",
            "relation": "edge relationship",
            "target": f"{node_b}",
            "directed": True,
            "label": f"{label}",
            "metadata": {
                "type": "edge type",
            }
        }
        graph_json["graph"]["edges"].append(edge)

    with open("json-graph-schema.json", "r", encoding="utf-8") as file:
        schema = json.load(file)

    validate(instance=graph_json, schema=schema)

    indent = None if minify_json else 4

    with open("network_graphjson.json", "w", encoding="utf-8") as file:
        json.dump(graph_json, file, indent=indent)

def create_gml(nodes: List[str], matrix: List[List[List[int]]]) -> None:
    gml_nodes = []
    gml_edges = []

    node_ids = {}
    for node_id, node_name in enumerate(nodes):
        node_ids[node_name] = node_id
        gml_node = f"""node
        [
            id {node_id}
            label "{node_name}"
        ]
        """
        gml_nodes.append(gml_node)

    for node_a, node_b, label in get_graph_edges(nodes, matrix):
        gml_edge = f"""edge
        [
            source {node_ids[node_a]}
            target {node_ids[node_b]}
            label "{label}"
            id "({node_a} -> {node_b})"
        ]
        """
        gml_edges.append(gml_edge)

    gml = f"""graph[
        directed 1
        {''.join(gml_nodes)}
        {''.join(gml_edges)}
    ]"""

    with open("network_gml.gml", "w", encoding="utf-8") as file:
        file.write(gml)

def print_example(nodes: List[str], matrix: List[List[List[str]]]) -> None:
    node_a_index = 0
    node_b_index = 1

    node_a = nodes[node_a_index]
    node_b = nodes[node_b_index]
    edges = matrix[node_a_index][node_b_index]

    print(f"Edges from ({node_a}) to ({node_b}) are of labels: {edges} ('' means no edge)")

def write_to_files(nodes: List[str], matrix: List[List[List[str]]], minify_json: bool):
    write_json(nodes, matrix, minify_json)
    create_graphjson(nodes, matrix, minify_json)
    create_gml(nodes, matrix)


def generate_dataset(num_nodes: int, max_connections_between_nodes: int, minify_json: bool) -> None:
    nodes = generate_column_names(num_nodes)
    matrix = generate_matrix(num_nodes, max_connections_between_nodes)
    write_to_files(nodes, matrix, minify_json)
    print_example(nodes, matrix)

if (__name__ == "__main__"):
    check_directory()
    generate_dataset(10, 1, True)
