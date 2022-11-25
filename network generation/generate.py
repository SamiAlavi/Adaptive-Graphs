from typing import List
from string import ascii_uppercase
import json
import numpy as np

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

def generate_matrix(num_nodes: int, max_connections_between_nodes: int) -> List[List[List[int]]]:
    matrix = np.random.randint(0, 10, (num_nodes, num_nodes, max_connections_between_nodes))

    return matrix

def write_json(nodes: List[str], matrix: List[List[List[int]]], minify_json: bool) -> None:
    data = {
        'nodes': nodes,
        'matrix': matrix.tolist()
    }
    indent = None if minify_json else 4

    with open("network.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=indent)

def print_example(nodes: List[str], matrix: List[List[List[int]]]) -> None:
    node_a_index = 0
    node_b_index = 1

    node_a = nodes[node_a_index]
    node_b = nodes[node_b_index]
    edges = matrix[node_a_index][node_b_index]

    print(f'Edges from ({node_a}) to ({node_b}) are of weights: {edges} (0 means no edge)')

def generate_dataset(num_nodes: int, max_connections_between_nodes: int, minify_json: bool) -> None:
    nodes = generate_column_names(num_nodes)
    matrix = generate_matrix(num_nodes, max_connections_between_nodes)
    write_json(nodes, matrix, minify_json)
    print_example(nodes, matrix)

if (__name__ == "__main__"):
    generate_dataset(10, 1, True)
