# from https://bradfieldcs.com/algos/graphs/prims-spanning-tree-algorithm/
import bloom_filter
import sys
import string
import random
from collections import defaultdict
from bitarray import bitarray
import heapq


class Graph:
    """
    Represents a Graph.

    Parameters:
    """

    def __init__(self, n, random=False):
        self.size = n
        if random:
            self.graph = self._generate_graph(n)
        else:
            self.graph = defaultdict(dict)
        self.n_edges = 0

    def __str__(self):
        return str(self.graph)

    def add_undirected_edge(self, source, sink, cost):
        self.graph[source][sink] = (cost, self.n_edges)
        self.graph[sink][source] = (cost, self.n_edges)
        self.n_edges += 1

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

        edge_idx = 0
        # Populate Graph
        for node in graph:
            n_neighbours = random.randint(min_neighbours, max_neighbours)

            for _ in range(n_neighbours):
                cost = random.randint(min_neighbours, max_cost)
                # We don't really care about duplicates, esp in large graphs b/c it'll be rare and just overwrite anyway
                neighbour = random.choice(list(graph.keys()))

                if neighbour != node:
                    graph[node][neighbour] = (cost, edge_idx)
                    graph[neighbour][node] = (cost, edge_idx)
                    edge_idx += 1

        graph[-1] = edge_idx  # Equivalent to # of edges. Probably bad practice but w/e
        self.n_edges = edge_idx
        print("Graph Generated.\n")
        return graph

    def _get_letter(self, n):
        result = []
        alphabet = string.ascii_uppercase

        while n > 0:
            n -= 1
            n, i = divmod(n, 26)
            result.append(alphabet[i])

        return "".join(result[::-1])

    # Remember: Cost[1] is edge idx
    @staticmethod
    def minimum_spanning_tree(graph_obj, starting_vertex, return_bit_graph=False):
        print("Starting to calculate regular MST...")
        graph = graph_obj.graph
        mst = defaultdict(set)
        visited = set([starting_vertex])
        edge_map = bitarray(graph_obj.n_edges)
        edge_map.setall(0)

        edges = [
            (cost[0], cost[1], starting_vertex, to)
            for to, cost in graph[starting_vertex].items()
        ]
        heapq.heapify(edges)
        total_cost = 0

        while edges:
            cost, edge_idx, frm, to = heapq.heappop(edges)

            if to not in visited:
                visited.add(to)
                total_cost += cost
                mst[frm].add(to)
                edge_map[edge_idx] = 1
                for to_next, cost in graph[to].items():
                    if to_next not in visited:
                        heapq.heappush(edges, (cost[0], cost[1], to, to_next))

        print(f"Set Space: {sys.getsizeof(visited)} Bytes\n")
        if not return_bit_graph:
            return total_cost, sys.getsizeof(visited)
        else:
            return total_cost, sys.getsizeof(visited), edge_map

    @staticmethod
    def bloom_minimum_spanning_tree(graph_obj, starting_vertex, return_bit_graph=False):
        print("Starting Bloom Filter MST...")
        graph = graph_obj.graph
        mst = defaultdict(set)
        visited = bloom_filter.BloomFilter(len(graph.keys()))  # Replace set w/ Bloom

        edge_map = bitarray(graph_obj.n_edges)
        edge_map.setall(0)

        edges = [
            (cost[0], cost[1], starting_vertex, to)
            for to, cost in graph[starting_vertex].items()
        ]
        heapq.heapify(edges)
        total_cost = 0

        while edges:
            cost, edge_idx, frm, to = heapq.heappop(edges)
            if not visited.probabilistic_contains(str(to)):
                visited.add(str(to))
                total_cost += cost
                mst[frm].add(to)
                edge_map[edge_idx] = 1
                for to_next, cost in graph[to].items():
                    if not visited.probabilistic_contains(str(to_next)):
                        heapq.heappush(edges, (cost[0], cost[1], to, to_next))

        edge_map_space = sys.getsizeof(edge_map)
        bf_space = visited.memory_used
        print(
            "Bloom Filter Space: " + str(bf_space),
            "Bloom Filter Filled: " + str(visited.percentage_filled),
            "Graph storage space: " + str(edge_map_space),
            "Total storage space: " + str(bf_space + edge_map_space),
        )
        print()
        if not return_bit_graph:
            return total_cost, visited.get_internals()
        else:
            return total_cost, visited.get_internals(), edge_map


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
    test_graph = Graph(10000)
    # print(test_graph)

    set_tree, set_cost, size = Graph.minimum_spanning_tree(test_graph.graph, "A")
    bf_tree, bf_cost, internals = Graph.bloom_minimum_spanning_tree(
        test_graph.graph, "A"
    )

    print(f"Set Tree, Set Cost: (too long), {set_cost}")
    print(f"BF Tree, BF Cost: (too long), {bf_cost}")
