"""
Anything to do with Graphs and Graph Nodes for this project 
"""


class GraphNode:
    """
    Represents a GraphNode.

    Parameters:
    - data: integer (tbd): Holds the pertinent data for this node
    - neighbours: (GraphNode, float) arr: Holds a list of the direct neighbours to this node (undirected)
    """

    def __init__(self, data=None, neighbours=[], reflexive=True):
        self.data = data
        self.neighbours = (
            neighbours  # Remember, Python passes objects by reference not value
        )
        if reflexive:
            list(map(lambda node: node.add_neighbours([self], False), neighbours))

    def add_neighbours(self, new_additions=[], reflexive=True):
        """
        Append neighbours to the list of neighbours. Allows for duplicates.

        returns: void
        """

        self.neighbours += new_additions

        if reflexive:
            list(map(lambda node: node.add_neighbours([self], False), new_additions))