from typing import Callable, Generator, Any
import networkx as nx
from networkx import DiGraph
import json
from graph_networkx import NetworkX

class Exporter(NetworkX):

    def export(self, network):
        try:
            file_type = network["file_type"]
            del(network["file_type"])
        except:
            raise Exception("Request JSON does not has 'file_type' key")

        if (file_type == "json"):
            return self.export_json_format(network)
        elif (file_type == "gml"):
            return self.export_networkx_formats(network, nx.generate_gml)
        elif (file_type == "graphml"):
            return self.export_networkx_formats(network, nx.generate_graphml)
        else:
            raise Exception(f"Exporting graph in '{file_type}' format is not supported")

    def export_json_format(self, network) -> bytes:
        return self.string_to_bytes(json.dumps(network, indent=2))

    def export_networkx_formats(self, network, generate: Callable[[DiGraph], Generator[Any | str, None, None]]) -> bytes:
        self.read_network_json(network)
        self.add_graph_nodes()
        self.add_graph_edges()
        generator = generate(self.graph)
        string = "\n".join(line for line in generator)
        return self.string_to_bytes(string)

    def string_to_bytes(self, string: str) -> bytes:
        return string.encode('utf-8')
