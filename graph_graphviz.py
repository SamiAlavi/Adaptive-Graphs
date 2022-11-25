from graph_base import BaseGraph
import graphviz

class GraphViz(BaseGraph):
    def __init__(self) -> None:
        super().__init__()
        self.graph = graphviz.Digraph(comment='Graph_GraphViz')

    def addGraphNodes(self) -> None:
        for node in super()._getGraphNodes():
            self.graph.node(node, node)

    def addGraphEdges(self) -> None:
        for nodeA, nodeB, weight in super()._getGraphEdges():
            self.graph.edge(nodeA, nodeB, label=str(weight))

    def printGraphProperties(self) -> None:
        print(self.graph.source)

    def drawGraph(self) -> None:
        # make sure graphviz is installed and is in PATH, https://www.graphviz.org/download/
        self.graph.render('graphs/graphviz.gv', view=True)


if (__name__ == "__main__"):
    graph = GraphViz()
    graph.readNetworkJson()
    graph.createGraph()
    graph.drawGraph()

