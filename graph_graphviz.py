from graph_base import BaseGraph
import graphviz

class GraphViz(BaseGraph):
    def __init__(self) -> None:
        super().__init__()
        self.graph = graphviz.Digraph(comment='Graph_GraphViz')

    def add_graph_nodes(self) -> None:
        for node in super()._get_graph_nodes():
            self.graph.node(node, node)

    def add_graph_edges(self) -> None:
        for nodeA, nodeB, weight in super()._get_graph_edges():
            self.graph.edge(nodeA, nodeB, label=str(weight))

    def print_graph_properties(self) -> None:
        print(self.graph.source)

    def draw_graph(self) -> None:
        # make sure graphviz is installed and is in PATH, https://www.graphviz.org/download/
        self.graph.render('graphs/graphviz.gv', view=True)


if (__name__ == "__main__"):
    graph = GraphViz()
    graph.read_network_json()
    graph.create_graph()
    graph.draw_graph()

