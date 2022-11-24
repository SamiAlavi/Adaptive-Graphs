from graph_networkx import NetworkX
from pyvis.network import Network

class Pyvis(NetworkX):
    def __init__(self) -> None:
        super().__init__()

    def drawGraph(self) -> None:
        net = Network(height="98vh")
        net.from_nx(self.graph, show_edge_weights=True)
        net.toggle_physics(True)
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
        net.set_options(pyvisOptions)
        #net.show_buttons()
        fileName = "graphs/Graph_Pyvis.html"
        net.show(fileName)


if (__name__ == "__main__"):
    graph = Pyvis()
    graph.readNetworkJson()
    graph.createGraph()
    graph.drawGraph()

