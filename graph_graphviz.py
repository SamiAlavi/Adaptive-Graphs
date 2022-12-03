import graphviz
import base64
from graph_base import BaseGraph

class GraphViz(BaseGraph):
    def __init__(self) -> None:
        super().__init__()
        self.graph = graphviz.Digraph(comment='Graph_GraphViz')

    def add_graph_nodes(self) -> None:
        for node in super()._get_graph_nodes():
            self.graph.node(node, node)

    def add_graph_edges(self) -> None:
        for node_a, node_b, weight in super()._get_graph_edges():
            self.graph.edge(node_a, node_b, label=str(weight))

    def print_graph_properties(self) -> None:
        print(self.graph.source)

    def draw_graph(self) -> None:
        # make sure graphviz is installed and is in PATH, https://www.graphviz.org/download/
        self.graph.render('graphs/graphviz.gv', view=True)

    def get_graph_data(self) -> str:
        graph_output = self.graph.pipe(format='png')
        data = base64.b64encode(graph_output).decode('utf-8')
        return f"data:image/png;base64,{data}"


if (__name__ == "__main__"):
    graph = GraphViz()
    graph.read_network_json()
    graph.create_graph()
    graph.draw_graph()
