from graph import GraphNode
import random

"""
Script to generate and then pickle custom, random graphs. TODO: Eventually, need to add command line arg support
"""


def generate_graph(n, max_neighbours=999):
    """
    Guarantees: This is a fully connected graph with one giant component, so one can start anywhere and connect all the nodes.
    """
    assert n >= max_neighbours + 1

    start_node = GraphNode(0)
    nodes = [start_node]
    n_start_neighbours = random.randint(1, max_neighbours - 1)
    nodes += [GraphNode(i, [start_node]) for i in range(1, n_start_neighbours + 1)]

    n -= n_start_neighbours + 1

    while n > 0:
        n_neighbours = random.randint(0, max_neighbours)
        n_neighbours = n_neighbours if n_neighbours <= n else n
        lower_bound = random.randint(0, len(nodes) - 1)
        upper_bound = random.randint(lower_bound, len(nodes))
        random_nodes = nodes[lower_bound:upper_bound]

        new_neighbours = [
            GraphNode(random.random(), random_nodes) for i in range(n_neighbours)
        ]

        nodes += new_neighbours

        n -= n_neighbours

    print([(node.data, list(map(lambda x: x.data, node.neighbours))) for node in nodes])


if __name__ == "__main__":
    generate_graph(10, 2)
