from string import ascii_uppercase
import json
import numpy as np

def colToExcel(col): # col is 1 based
    excelCol = str()
    div = col 
    while div:
        (div, mod) = divmod(div-1, 26) # will return (x, 0 .. 25)
        excelCol = ascii_uppercase[mod] + excelCol

    return excelCol
from typing import List

def generateColumnNames(numCols: int) -> List[str]:
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

def generateMatrix(numNodes: int, maxConnectionsBetweenNodes: int) -> List[List[List[int]]]:
    matrix = np.random.randint(0, 10, (numNodes, numNodes, maxConnectionsBetweenNodes))

    return matrix

def writeJson(nodes: List[str], matrix: List[List[List[int]]], minifyJson: bool):
    data = {
        'nodes': nodes,
        'matrix': matrix.tolist()
    }
    indent = None if minifyJson else 4

    with open("network.json", "w") as file:
        json.dump(data, file, indent=indent)

def printExample(nodes: List[str], matrix: List[List[List[int]]]):
    nodeAIndex = 0
    nodeBIndex = 1

    nodeA = nodes[nodeAIndex]
    nodeB = nodes[nodeBIndex]
    edges = matrix[nodeAIndex][nodeBIndex]

    print(f'Edges from ({nodeA}) to ({nodeB}) are of weights: {edges} (0 means no edge)')

def generateDataset(numNodes: int, maxConnectionsBetweenNodes: int, minifyJson: bool):
    nodes = generateColumnNames(numNodes)
    matrix = generateMatrix(numNodes, maxConnectionsBetweenNodes)
    writeJson(nodes, matrix, minifyJson)
    printExample(nodes, matrix)

if (__name__ == "__main__"):
    generateDataset(10, 1, True)