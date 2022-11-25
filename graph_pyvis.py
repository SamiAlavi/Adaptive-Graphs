from graph_networkx import NetworkX
from pyvis.network import Network

class Pyvis(NetworkX):
    def __init__(self) -> None:
        super().__init__()
        self.net = Network(height="98vh")

    def drawGraph(self) -> None:
        self.net.from_nx(self.graph, show_edge_weights=True)
        self.net.toggle_physics(True)
        pyvisOptions = """
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
        self.net.set_options(pyvisOptions)
        #net.show_buttons()
        fileName = "graphs/Graph_Pyvis.html"
        self.net.show(fileName)


if (__name__ == "__main__"):
    graph = Pyvis()
    graph.readNetworkJson()
    graph.createGraph()
    graph.drawGraph()

