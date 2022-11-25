from pyvis.network import Network
from graph_networkx import NetworkX

class Pyvis(NetworkX):
    def __init__(self) -> None:
        super().__init__()
        self.net = Network(height="98vh")

    def draw_graph(self) -> None:
        self.net.from_nx(self.graph, show_edge_weights=True)
        self.net.toggle_physics(True)
        pyvis_options = """
            options = {
                "edges": {
                    "arrows": {
                        "to": {
                            "enabled": true
                        }
                    },
                    "color": {
                        "inherit": true
                    },
                    "font": {
                        "strokeWidth": 0.1
                    },
                    "selfReferenceSize": null,
                    "selfReference": {
                        "angle": 0.7853981633974483
                    },
                    "smooth": {
                        "forceDirection": "none"
                    }
                },
                "physics": {
                    "barnesHut": {
                        "gravitationalConstant": -30000
                    },
                    "minVelocity": 0.75
                }
            }
        """
        self.net.set_options(pyvis_options)
        #net.show_buttons()
        file_name = "graphs/Graph_Pyvis.html"
        self.net.show(file_name)


if (__name__ == "__main__"):
    graph = Pyvis()
    graph.readNetworkJson()
    graph.createGraph()
    graph.draw_graph()
