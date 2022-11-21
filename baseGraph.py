import json
from abc import ABCMeta, abstractmethod
from typing import Generator, Tuple

class BaseGraph(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.__readNetworkJson()

    def __readNetworkJson(self) -> dict:
        jsonPath = "network generation/network.json"

        with open(jsonPath, 'r') as file:
            network = json.load(file)
            
        self.__nodes = network["nodes"]
        self.__matrix = network["matrix"]

    def _getGraphNodes(self) -> Generator[str, None, None]:
        for node in self.__nodes:
            yield node

    def _getGraphEdges(self) -> Generator[Tuple[str, str, int], None, None]:
        numNodes = len(self.__nodes)
        for nodeAIndex in range(numNodes):
            nodeA = self.__nodes[nodeAIndex]
            for nodeBIndex in range(numNodes):
                nodeB = self.__nodes[nodeBIndex]
                weights = self.__matrix[nodeAIndex][nodeBIndex]
                for weight in weights:
                    if (weight != 0):
                        yield nodeA, nodeB, weight

    def createGraph(self) -> None:
        try:
            self.addGraphNodes()
            self.addGraphEdges()
            self.printGraphProperties()
        except Exception as e:
            print(str(e))

    @abstractmethod
    def addGraphNodes(self) -> None:
        pass

    @abstractmethod
    def addGraphEdges(self) -> None:
        pass

    @abstractmethod
    def printGraphProperties(self) -> None:
        pass

    @abstractmethod
    def drawGraph(self) -> None:
        pass