import json
from abc import ABCMeta, abstractmethod
from typing import Generator, Tuple

class BaseGraph(metaclass=ABCMeta):

    def __init__(self) -> None:
        pass

    def read_network_json(self) -> dict:
        json_path = "network generation/network.json"

        with open(json_path, 'r') as file:
            network = json.load(file)

        self.__nodes = network["nodes"]
        self.__matrix = network["matrix"]

    def _get_graph_nodes(self) -> Generator[str, None, None]:
        for node in self.__nodes:
            yield node

    def _get_graph_edges(self) -> Generator[Tuple[str, str, int], None, None]:
        num_nodes = len(self.__nodes)
        for node_a_index in range(num_nodes):
            node_a = self.__nodes[node_a_index]
            for node_b_index in range(num_nodes):
                node_b = self.__nodes[node_b_index]
                weights = self.__matrix[node_a_index][node_b_index]
                for weight in weights:
                    if (weight > 0):
                        yield node_a, node_b, weight

    def create_graph(self) -> None:
        try:
            self.add_graph_nodes()
            self.add_graph_edges()
            self.print_graph_properties()
        except Exception as exception:
            print(str(exception))

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
