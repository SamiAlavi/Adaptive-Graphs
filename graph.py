import json
from abc import ABCMeta, abstractmethod

class BaseGraph(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.__readNetworkJson()

    def __readNetworkJson(self) -> dict:
        jsonPath = "network generation/network.json"

        with open(jsonPath, 'r') as file:
            network = json.load(file)
            
        self.nodes = network["nodes"]
        self.matrix = network["matrix"]

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
        
    @abstractmethod
    def createGraph(self) -> None:
        pass