from pyvis.network import Network
from graph_networkx import NetworkX

# TODO 1: Update code as necessary after package gets updated
class Pyvis(NetworkX):
    def __init__(self) -> None:
        super().__init__()
        self.network = Network(height="98vh")

    def create_graph(self) -> None:
        super().create_graph()
        self.network.from_nx(self.graph, show_edge_weights=True)
        self.network.toggle_physics(True)
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
        self.network.set_options(pyvis_options)
        #net.show_buttons()

    def draw_graph(self) -> None:
        from os import getcwd
        file_path = f"{getcwd()}/graphs/Graph_Pyvis.html"
        self.network.write_html(file_path)
        self.network.show(file_path)

    def get_graph_data(self) -> str:
        return self.network.generate_html()


if (__name__ == "__main__"):
    graph = Pyvis()
    graph.read_network_json()
    graph.create_graph()
    graph.draw_graph()
