from typing import Any
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
from graph_base import BaseGraph

class NetworkX(BaseGraph):
    def __init__(self) -> None:
        super().__init__()
        self.graph = nx.DiGraph()

    def add_graph_nodes(self) -> None:
        for node in super()._get_graph_nodes():
            self.graph.add_node(node)

    def add_graph_edges(self) -> None:
        for node_a, node_b, weight in super()._get_graph_edges():
            self.graph.add_edge(node_a, node_b, label=weight)

    def print_graph_properties(self) -> None:
        print("Total number of nodes: ", int(self.graph.number_of_nodes()))
        print("Total number of edges: ", int(self.graph.number_of_edges()))
        print("Degree for all nodes: ", dict(self.graph.degree()))

    # https://stackoverflow.com/a/60641770/20621283
    def my_draw_networkx_edge_labels(
        self,
        G,
        pos,
        edge_labels=None,
        label_pos=0.5,
        font_size=10,
        font_color="black",
        font_family="sans-serif",
        font_weight="normal",
        alpha=None,
        bbox=None,
        horizontalalignment="center",
        verticalalignment="center",
        ax=None,
        rotate=True,
        clip_on=True,
        rad=0
    ):
        """Draw edge labels.

        Parameters
        ----------
        G : graph
            A networkx graph

        pos : dictionary
            A dictionary with nodes as keys and positions as values.
            Positions should be sequences of length 2.

        edge_labels : dictionary (default={})
            Edge labels in a dictionary of labels keyed by edge two-tuple.
            Only labels for the keys in the dictionary are drawn.

        label_pos : float (default=0.5)
            Position of edge label along edge (0=head, 0.5=center, 1=tail)

        font_size : int (default=10)
            Font size for text labels

        font_color : string (default='k' black)
            Font color string

        font_weight : string (default='normal')
            Font weight

        font_family : string (default='sans-serif')
            Font family

        alpha : float or None (default=None)
            The text transparency

        bbox : Matplotlib bbox, optional
            Specify text box properties (e.g. shape, color etc.) for edge labels.
            Default is {boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0)}.

        horizontalalignment : string (default='center')
            Horizontal alignment {'center', 'right', 'left'}

        verticalalignment : string (default='center')
            Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

        ax : Matplotlib Axes object, optional
            Draw the graph in the specified Matplotlib axes.

        rotate : bool (deafult=True)
            Rotate edge labels to lie parallel to edges

        clip_on : bool (default=True)
            Turn on clipping of edge labels at axis boundaries

        Returns
        -------
        dict
            `dict` of labels keyed by edge

        Examples
        --------
        >>> G = nx.dodecahedral_graph()
        >>> edge_labels = nx.draw_networkx_edge_labels(self.graph, pos=nx.spring_layout(G))

        Also see the NetworkX drawing examples at
        https://networkx.org/documentation/latest/auto_examples/index.html

        See Also
        --------
        draw
        draw_networkx
        draw_networkx_nodes
        draw_networkx_edges
        draw_networkx_labels
        """

        if ax is None:
            ax = plt.gca()
        if edge_labels is None:
            labels = {(u, v): d for u, v, d in G.edges(data=True)}
        else:
            labels = edge_labels
        text_items = {}
        for (n1, n2), label in labels.items():
            (x1, y1) = pos[n1]
            (x2, y2) = pos[n2]
            (x, y) = (
                x1 * label_pos + x2 * (1.0 - label_pos),
                y1 * label_pos + y2 * (1.0 - label_pos),
            )
            pos_1 = ax.transData.transform(np.array(pos[n1]))
            pos_2 = ax.transData.transform(np.array(pos[n2]))
            linear_mid = 0.5*pos_1 + 0.5*pos_2
            d_pos = pos_2 - pos_1
            rotation_matrix = np.array([(0,1), (-1,0)])
            ctrl_1 = linear_mid + rad*rotation_matrix@d_pos
            ctrl_mid_1 = 0.5*pos_1 + 0.5*ctrl_1
            ctrl_mid_2 = 0.5*pos_2 + 0.5*ctrl_1
            bezier_mid = 0.5*ctrl_mid_1 + 0.5*ctrl_mid_2
            (x, y) = ax.transData.inverted().transform(bezier_mid)

            if (n1 == n2):
                y+=0.1

            if rotate:
                # in degrees
                angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
                # make label orientation "right-side-up"
                if angle > 90:
                    angle -= 180
                if angle < -90:
                    angle += 180
                # transform data coordinate angle to screen coordinate angle
                xy = np.array((x, y))
                trans_angle = ax.transData.transform_angles(
                    np.array((angle,)), xy.reshape((1, 2))
                )[0]
            else:
                trans_angle = 0.0
            # use default box of white with white border
            if bbox is None:
                bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
            if not isinstance(label, str):
                label = str(label)  # this makes "1" and 1 labeled the same

            t = ax.text(
                x,
                y,
                label,
                size=font_size,
                color=font_color,
                family=font_family,
                weight=font_weight,
                alpha=alpha,
                horizontalalignment=horizontalalignment,
                verticalalignment=verticalalignment,
                rotation=trans_angle,
                transform=ax.transData,
                bbox=bbox,
                zorder=1,
                clip_on=clip_on,
            )
            text_items[(n1, n2)] = t

        ax.tick_params(
            axis="both",
            which="both",
            bottom=False,
            left=False,
            labelbottom=False,
            labelleft=False,
        )

        return text_items


    def draw_graph(self) -> None:
        seed = 13648  # Seed random number generators for reproducibility
        arc_rad = 0.25
        bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0), alpha=0.5)

        self.fig = plt.figure("Graph_NetworkX", figsize=(20,20))        
        pos = nx.spring_layout(self.graph, seed=seed)        
        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)

        edges = self.graph.edges()
        curved_edges = [edge for edge in edges if reversed(edge) in edges]
        straight_edges = list(set(edges) - set(curved_edges))
        nx.draw_networkx_edges(self.graph, pos, edgelist=straight_edges, alpha=0.9)
        nx.draw_networkx_edges(self.graph, pos, edgelist=curved_edges, alpha=0.5, connectionstyle=f'arc3, rad = {arc_rad}')

        edge_weights = nx.get_edge_attributes(self.graph, 'label')
        curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
        straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}
        self.my_draw_networkx_edge_labels(self.graph, pos, edge_labels=curved_edge_labels,rotate=False, font_color='red', alpha=0.9, bbox=bbox, rad=arc_rad)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=straight_edge_labels,rotate=False, font_color='red', alpha=0.9, bbox=bbox)

    def get_graph_data(self) -> str:
        img = BytesIO()
        self.fig.savefig(img, bbox_inches='tight', pad_inches=0, format="png")
        img.seek(0) # writing moved the cursor to the end of the file, reset
        plt.clf() # clear pyplot
        data = base64.b64encode(img.getbuffer()).decode("ascii") # Embed the result in the html output.
        return f"data:image/png;base64,{data}"

if (__name__ == "__main__"):
    graph = NetworkX()
    graph.read_network_json()
    graph.create_graph()
    graph.draw_graph()
    plt.show()
else:
    matplotlib.use('Agg') # non-GUI backend
