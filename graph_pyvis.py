from pyvis.network import Network
from graph_networkx import NetworkX

# TODO 1: Update code as necessary after package gets updated
class Pyvis(NetworkX):

    def set_options(self, options: dict) -> None:
        self.options = {
            "height": "600px",
            "width": "100%",
            "directed": True,
            "notebook": False,
            "neighborhood_highlight": False,
            "select_menu": False,
            "filter_menu": False,
            "bgcolor": "#ffffff",
            "font_color": False,
            "layout": None,
            "heading": "",
            "cdn_resources": "remote"
        }

        filtered_keys = ["height", "width", "neighborhood_highlight", "bgcolor", "font_color"]
        
        for key in filtered_keys:
            if (key in options):
                self.options[key] = options[key]


    def __init__(self, options: dict={}) -> None:
        super().__init__()
        self.set_options(options)

        self.network = Network(
            height=self.options["height"],
            width=self.options["width"],
            directed=self.options["directed"],
            notebook=self.options["notebook"],
            neighborhood_highlight=self.options["neighborhood_highlight"],
            select_menu=self.options["select_menu"],
            filter_menu=self.options["filter_menu"],
            bgcolor=self.options["bgcolor"],
            font_color=self.options["font_color"],
            layout=self.options["layout"],
            heading=self.options["heading"],
            cdn_resources=self.options["cdn_resources"]
            )

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
