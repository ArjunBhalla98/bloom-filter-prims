# from https://bradfieldcs.com/algos/graphs/prims-spanning-tree-algorithm/
import bloom_filter
import sys
import string
import random
from collections import defaultdict
import heapq


class Graph:
    """
    Represents a Graph.

    Parameters:
    """

    def __init__(self, n):
        self.size = n
        self.graph = self._generate_graph(n)

    def __str__(self):
        return str(self.graph)

    def _generate_graph(
        self, n, min_neighbours=1, max_neighbours=25, min_cost=1, max_cost=50
    ):
        """
        Generate all n nodes, then for each of them choose a random 
        O(n^2) runtime
        """
        print("Starting Graph Generation...")
        # Initialise Graph DS
        graph = {}
        for i in range(n):
            graph[self._get_letter(i)] = {}

        # Populate Graph
        for node in graph:
            n_neighbours = random.randint(min_neighbours, max_neighbours)

            for _ in range(n_neighbours):
                cost = random.randint(min_neighbours, max_cost)
                # We don't really care about duplicates, esp in large graphs b/c it'll be rare and just overwrite anyway
                neighbour = random.choice(list(graph.keys()))

                if neighbour != node:
                    graph[node][neighbour] = cost
                    graph[neighbour][node] = cost
        print("Graph Generated.")
        return graph

    def _get_letter(self, n):
        result = []
        alphabet = string.ascii_uppercase

        while n > 0:
            n -= 1
            n, i = divmod(n, 26)
            result.append(alphabet[i])

        return "".join(result[::-1])

    @staticmethod
    def minimum_spanning_tree(graph, starting_vertex):
        print("Starting to calculate regular MST...")
        mst = defaultdict(set)
        visited = set([starting_vertex])
        edges = [
            (cost, starting_vertex, to) for to, cost in graph[starting_vertex].items()
        ]
        heapq.heapify(edges)
        total_cost = 0

        while edges:
            cost, frm, to = heapq.heappop(edges)
            if to not in visited:
                visited.add(to)
                total_cost += cost
                mst[frm].add(to)
                for to_next, cost in graph[to].items():
                    if to_next not in visited:
                        heapq.heappush(edges, (cost, to, to_next))

        print(f"Set Space: {sys.getsizeof(visited)} Bytes")
        return mst, total_cost, sys.getsizeof(visited)

    @staticmethod
    def bloom_minimum_spanning_tree(graph, starting_vertex):
        print("Starting Bloom Filter MST...")
        mst = defaultdict(set)
        visited = bloom_filter.BloomFilter(len(graph.keys()))  # Replace set w/ Bloom
        edges = [
            (cost, starting_vertex, to) for to, cost in graph[starting_vertex].items()
        ]
        heapq.heapify(edges)
        total_cost = 0

        while edges:
            cost, frm, to = heapq.heappop(edges)
            if not visited.probabilistic_contains(to):
                visited.add(to)
                total_cost += cost
                mst[frm].add(to)
                for to_next, cost in graph[to].items():
                    if not visited.probabilistic_contains(to_next):
                        heapq.heappush(edges, (cost, to, to_next))

        print(
            "Bloom Filter Space: " + str(visited.memory_used),
            "Bloom Filter Filled: " + str(visited.percentage_filled),
        )
        return mst, total_cost, visited.get_internals()


example_graph = {
    "A": {"B": 2, "C": 3},
    "B": {"A": 2, "C": 1, "D": 1, "E": 4},
    "C": {"A": 3, "B": 1, "F": 5},
    "D": {"B": 1, "E": 1},
    "E": {"B": 4, "D": 1, "F": 1},
    "F": {"C": 5, "E": 1, "G": 1},
    "G": {"F": 1},
}

if __name__ == "__main__":
    test_graph = Graph(1000000)
    # print(test_graph)

    set_tree, set_cost = Graph.minimum_spanning_tree(test_graph.graph, "A")
    bf_tree, bf_cost = Graph.bloom_minimum_spanning_tree(test_graph.graph, "A")

    print(f"Set Tree, Set Cost: (too long), {set_cost}")
    print(f"BF Tree, BF Cost: (too long), {bf_cost}")
