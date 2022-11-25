from string import ascii_uppercase
import json
import numpy as np

def column_to_excel(col): # col is 1 based
    excelCol = str()
    div = col 
    while div:
        (div, mod) = divmod(div-1, 26) # will return (x, 0 .. 25)
        excelCol = ascii_uppercase[mod] + excelCol

    return excelCol
from typing import List

def generate_column_names(numCols: int) -> List[str]:
    titles = list(ascii_uppercase)

    if (numCols <= 26):
        return titles[:numCols]

    numCols-=26
    times = 0

    while (numCols > 0):
        sublist = [titles[times]+char for char in ascii_uppercase][:numCols]
        titles.extend(sublist)
        numCols-=26
        times+=1

    return titles

def generate_matrix(numNodes: int, maxConnectionsBetweenNodes: int) -> List[List[List[int]]]:
    matrix = np.random.randint(0, 10, (numNodes, numNodes, maxConnectionsBetweenNodes))

    return matrix

def write_json(nodes: List[str], matrix: List[List[List[int]]], minifyJson: bool):
    data = {
        'nodes': nodes,
        'matrix': matrix.tolist()
    }
    indent = None if minifyJson else 4

    with open("network.json", "w") as file:
        json.dump(data, file, indent=indent)

def print_example(nodes: List[str], matrix: List[List[List[int]]]):
    nodeAIndex = 0
    nodeBIndex = 1

    nodeA = nodes[nodeAIndex]
    nodeB = nodes[nodeBIndex]
    edges = matrix[nodeAIndex][nodeBIndex]

    print(f'Edges from ({nodeA}) to ({nodeB}) are of weights: {edges} (0 means no edge)')

def generate_dataset(numNodes: int, maxConnectionsBetweenNodes: int, minifyJson: bool):
    nodes = generate_column_names(numNodes)
    matrix = generate_matrix(numNodes, maxConnectionsBetweenNodes)
    write_json(nodes, matrix, minifyJson)
    print_example(nodes, matrix)

if (__name__ == "__main__"):
    generate_dataset(10, 1, True)