from graph import BaseGraph
import graphviz

class GraphViz(BaseGraph):
    def __init__(self) -> None:
        super().__init__()

    def addGraphNodes(self) -> None:
        for node in self.nodes:
            self.graph.node(node, node)

    def addGraphEdges(self) -> None:
        numNodes = len(self.nodes)
        for nodeAIndex in range(numNodes):
            nodeA = self.nodes[nodeAIndex]
            for nodeBIndex in range(numNodes):
                nodeB = self.nodes[nodeBIndex]
                weights = self.matrix[nodeAIndex][nodeBIndex]
                for weight in weights:
                    if (weight != 0):
                        self.graph.edge(nodeA, nodeB, label=str(weight))

    def printGraphProperties(self) -> None:
        print(self.graph.source)

    def createGraph(self) -> None:
        self.graph = graphviz.Digraph(comment='Graph_GraphViz')

        self.addGraphNodes()
        self.addGraphEdges()
        self.printGraphProperties()

    def drawGraph(self) -> None:
        # make sure graphviz is installed and is in PATH, https://www.graphviz.org/download/
        self.graph.render('graphs/graphviz.gv', view=True)


if (__name__ == "__main__"):
    graph = GraphViz()
    graph.createGraph()
    graph.drawGraph()

