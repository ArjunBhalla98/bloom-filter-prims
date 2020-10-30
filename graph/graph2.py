# from https://bradfieldcs.com/algos/graphs/prims-spanning-tree-algorithm/
import bloom_filter
import sys
from collections import defaultdict
import heapq


def minimum_spanning_tree(graph, starting_vertex):
    mst = defaultdict(set)
    visited = set([starting_vertex])
    edges = [(cost, starting_vertex, to) for to, cost in graph[starting_vertex].items()]
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
    return mst, cost


def bloom_minimum_spanning_tree(graph, starting_vertex):
    mst = defaultdict(set)
    visited = bloom_filter.BloomFilter(len(graph.keys()))  # Replace set w/ Bloom
    edges = [(cost, starting_vertex, to) for to, cost in graph[starting_vertex].items()]
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
    return mst, cost


example_graph = {
    "A": {"B": 2, "C": 3},
    "B": {"A": 2, "C": 1, "D": 1, "E": 4},
    "C": {"A": 3, "B": 1, "F": 5},
    "D": {"B": 1, "E": 1},
    "E": {"B": 4, "D": 1, "F": 1},
    "F": {"C": 5, "E": 1, "G": 1},
    "G": {"F": 1},
}

set_tree, set_cost = minimum_spanning_tree(example_graph, "D")
bf_tree, bf_cost = bloom_minimum_spanning_tree(example_graph, "D")

print(f"Set Tree, Set Cost: {set_tree}, {set_cost}")
print(f"BF Tree, BF Cost: {bf_tree}, {bf_cost}")
