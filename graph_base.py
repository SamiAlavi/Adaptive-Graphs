import json
from abc import ABCMeta, abstractmethod
from typing import Generator, Tuple

class BaseGraph(metaclass=ABCMeta):

    def __init__(self) -> None:
        pass

    def read_network_json(self) -> dict:
        jsonPath = "network generation/network.json"

        with open(jsonPath, 'r') as file:
            network = json.load(file)

        self.__nodes = network["nodes"]
        self.__matrix = network["matrix"]

    def _get_graph_nodes(self) -> Generator[str, None, None]:
        for node in self.__nodes:
            yield node

    def _get_graph_edges(self) -> Generator[Tuple[str, str, int], None, None]:
        numNodes = len(self.__nodes)
        for nodeAIndex in range(numNodes):
            nodeA = self.__nodes[nodeAIndex]
            for nodeBIndex in range(numNodes):
                nodeB = self.__nodes[nodeBIndex]
                weights = self.__matrix[nodeAIndex][nodeBIndex]
                for weight in weights:
                    if (weight > 0):
                        yield nodeA, nodeB, weight

    def create_graph(self) -> None:
        try:
            self.add_graph_nodes()
            self.add_graph_edges()
            self.print_graph_properties()
        except Exception as e:
            print(str(e))

    @abstractmethod
    def add_graph_nodes(self) -> None:
        pass

    @abstractmethod
    def add_graph_edges(self) -> None:
        pass

    @abstractmethod
    def print_graph_properties(self) -> None:
        pass

    @abstractmethod
    def draw_graph(self) -> None:
        pass
