import json
from abc import ABCMeta, abstractmethod
from typing import Generator, Tuple

class BaseGraph(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.__nodes = []
        self.__matrix = []

    def read_network_json(self, network=None) -> dict:
        if (not network):
            json_path = "network generation/network.json"

            with open(json_path, "r", encoding="utf-8") as file:
                network = json.load(file)

        self.__nodes = network["nodes"]
        self.__matrix = network["matrix"]

    def _get_graph_nodes(self) -> Generator[str, None, None]:
        for node in self.__nodes:
            yield node

    def _get_graph_edges(self) -> Generator[Tuple[str, str, str], None, None]:
        num_nodes = len(self.__nodes)
        for node_a_index in range(num_nodes):
            node_a = self.__nodes[node_a_index]
            for node_b_index in range(num_nodes):
                node_b = self.__nodes[node_b_index]
                labels = self.__matrix[node_a_index][node_b_index]
                for label in labels:
                    if (label != ''):
                        yield node_a, node_b, label

    def create_graph(self) -> None:
        self.add_graph_nodes()
        self.add_graph_edges()
        self.print_graph_properties()

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

    @abstractmethod
    def get_graph_data(self) -> str:
        pass
