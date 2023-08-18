import matplotlib.pyplot as plt
import os
import time
import random
import sys
from graph import Graph

"""
Class for running various tests for the different MST methods, and plotting and saving graphs of those metrics locally.
TODO: 
1) Add nice command line logic to get different params / methods instead of having to change code
2) Implement more tests
3) Implement stat saving (pickle or txt) just to save having to re-process everything
"""


class MetricRunner:
    def __init__(self):
        pass

    def cost_size_compare(
        self, graphs:list[Graph], map_edges=False
    ):
        # Index of all of these corresponds to the relative graph size (i.e. x[0] is the result for mst(graph(start)))
        graph_size = []
        basic_prims_space = []
        basic_prims_cost = []
        bloom_prims_space = []
        bloom_prims_cost = []
        bloom_prims_stats = []

        # Counts the *absolute number* of edges that are missing in the bloom filter version
        if map_edges:
            edge_diff = []
            total_edges = []

        for graph in graphs:
            print("Graph # of Nodes: " + str(graph.size))
            graph_size.append(graph.size)

            if not map_edges:
                basic_cost, space = Graph.minimum_spanning_tree(graph, "0")
                bloom_cost, bloom_stats = Graph.bloom_minimum_spanning_tree(graph, "0")
            else:
                basic_cost, space, basic_edges = Graph.minimum_spanning_tree(
                    graph, "0", True
                )
                (
                    bloom_cost,
                    bloom_stats,
                    bloom_edges,
                    bloom_total_space,
                ) = Graph.bloom_minimum_spanning_tree(graph, "0", True)
                bloom_stats["space"] += sys.getsizeof(bloom_edges)
                edge_diff.append(abs(basic_edges.count() - bloom_edges.count()))
                total_edges.append(basic_edges.count())

            basic_prims_space.append(space)
            basic_prims_cost.append(basic_cost)

            bloom_prims_space.append(bloom_total_space)
            bloom_prims_cost.append(bloom_cost)
            bloom_prims_stats.append(bloom_stats)

            print("--------------------------------------")
        

        if not map_edges:
            return_obj = {
                    "graph_size": graph_size,
                    "basic_prims_space": basic_prims_space,
                    "basic_prims_cost": basic_prims_cost,
                    "bloom_prims_space": bloom_prims_space,
                    "bloom_prims_cost": bloom_prims_cost,
                    "bloom_prims_stats": bloom_prims_stats,
            }
        else:
            return_obj = {
                    "graph_size": graph_size,
                    "basic_prims_space": basic_prims_space,
                    "basic_prims_cost": basic_prims_cost,
                    "bloom_prims_space": bloom_prims_space,
                    "bloom_prims_cost": bloom_prims_cost,
                    "bloom_prims_stats": bloom_prims_stats,
                    "edge_diff": edge_diff,
                    "total_edges": total_edges,
            }
        

        with open("sparse_results.txt", "a") as f:
            f.write(str(return_obj))
        
        print(list(return_obj.values()))
        return list(return_obj.values())


class ChartGenerator:
    def __init__(self, image_path, graphs = []):
        self.metric_runner = MetricRunner()
        self.image_path = image_path
        self.data = {}
        self.graphs = graphs # list of graph objects to get metrics on

    def get_data(self, map_edges=True):
        if not map_edges:
            (
                g_size,
                ba_space,
                ba_cost,
                bl_space,
                bl_cost,
                bl_stats,
            ) = self.metric_runner.cost_size_compare(self.graphs)
        else:
            (
                g_size,
                ba_space,
                ba_cost,
                bl_space,
                bl_cost,
                bl_stats,
                edge_diff,
                total_edges,
            ) = self.metric_runner.cost_size_compare(self.graphs, map_edges=True)
            self.data["edge_diff"] = edge_diff
            self.data["n_edges"] = total_edges
        print(self.data)
        self.data["g_size"] = g_size
        self.data["ba_space"] = ba_space
        self.data["ba_cost"] = ba_cost
        self.data["bl_space"] = bl_space
        self.data["bl_cost"] = bl_cost
        self.data["bl_stats"] = bl_stats

    # Note: costs are very graph specific (obviously) and thus are not as good indicators of our algo's effectiveness. # edges is more absolute / varies with sparsity
    def plot_costs(self):
        self.plot_comparison(
            self.data["g_size"],
            self.data["ba_cost"],
            self.data["bl_cost"],
            "Basic",
            "Bloom Filter",
            "Graph Size (# Nodes)",
            "Cost of MST",
            "Graph Size vs Calculated Cost",
            f"cost{self.data['g_size'][-1]//1000}k.png",
        )

    def plot_edge_diff(self):
        assert "edge_diff" in self.data

        self.plot_singular(
            self.data["n_edges"],
            self.data["edge_diff"],
            "Absolute difference in edge set size",
            "Graph Size (# Edges in MST)",
            "Graph Size vs Edge Set Difference",
            f"edges{self.data['g_size'][-1]//1000000}m.png",
        )

    def plot_space(self):
        self.plot_comparison(
            self.data["g_size"],
            self.data["ba_space"],
            self.data["bl_space"],
            "Basic",
            "Bloom Filter",
            "Graph Size (# Nodes)",
            "Space Consumed (Bytes)",
            "Graph Size vs Space Consumed",
            f"space{self.data['g_size'][-1]//1000000}m.png",
        )

    ##### GENERIC METHODS ######
    def plot_singular(self, x, y, y_ax_label, x_ax_label, title, filename):
        plt.plot(x, y, color="b", marker=".")
        plt.title(title)
        plt.xlabel(x_ax_label)
        plt.ylabel(y_ax_label)
        plt.legend()
        plt.savefig(self.image_path + filename)
        plt.clf()
        print(self.data["bl_stats"])

    def plot_comparison(
        self, x, y1, y2, y1_label, y2_label, x_ax_label, y_ax_label, title, filename
    ):
        plt.plot(x, y1, color="orange", marker=".", label=y1_label)
        plt.plot(x, y2, color="b", marker="v", label=y2_label)
        plt.title(title)
        plt.xlabel(x_ax_label)
        plt.ylabel(y_ax_label)
        plt.legend()
        plt.savefig(self.image_path + filename)
        plt.clf()
        # print(self.data["bl_stats"])


if __name__ == "__main__":
    random.seed(3391)
    # test_graph = Graph(10000)
    # # print(test_graph)
    graph_files = [
        # "1000000_verts_sparse.txt",
        # "2000000_verts_sparse.txt",
        # "3000000_verts_sparse.txt",
        # "4000000_verts_sparse.txt",
        # "5000000_verts_sparse.txt",
        # "6000000_verts_sparse.txt",
        # "7000000_verts_sparse.txt",
        # "8000000_verts_sparse.txt",
        # "9000000_verts_sparse.txt",
        # "10000000_verts_sparse.txt",
    ]

    graph_files.reverse()

    data_dir = "data"


    # for graph_file in graph_files:
    #     graphs = []
    #     print(f"Processing graph file {graph_file}...")

    #     with open(os.path.join(data_dir, graph_file), "r") as fp:
    #         n_verts = int(graph_file[:int(graph_file.find("_"))])
    #         graph = Graph(n_verts)
    #         graph.stream_ingest_graph(fp)
    #         graphs.append(graph)
        
    #     plotter = ChartGenerator("./results_2023/", graphs)
    #     plotter.get_data(map_edges=True)
    #     plotter.plot_space()
    #     plotter.plot_edge_diff()
        # set_cost, size = Graph.minimum_spanning_tree(graph, 0)
        # bf_cost, internals = Graph.bloom_minimum_spanning_tree(
        #     graph, 0
        # )
    # plotter.plot_costs()
    plotter = ChartGenerator("./results_2023/", [])
    # plotter.plot_singular(
    #         [814817,1619565, 2396625, 3212885, 4000236, 5101912, 6109280, 7081825, 8291108, 9289165],
    #         [1553, 3013, 4448, 6016, 7474, 9001, 10212, 12010, 13814, 15005],
    #         "Absolute difference in edge set size",
    #         "Graph Size (# Nodes)",
    #         "Graph Size vs Edge Set Difference",
    #         f"edges10m.png",
    #     )
    plotter.plot_comparison(
        [814817,1619565, 2396625, 3212885, 4000236, 5101912, 6109280, 7081825, 8291108, 9289165],
        [33554648,67109080,67109080,134217944,134217944,268435888,268435888,536871776,536871776,1073743552],
        [1728455,3519847,5306319,7157922,8988600,11499320,13795112,16011542,18767498,21042070],
        "Basic",
        "Bloom Filter",
        "Graph Size (# Nodes)",
        "Space Consumed (Bytes)",
        "Graph Size vs Auxilliary Space Consumed",
        f"auxspace10m.png",
    )

    plotter.plot_comparison(
        [814817,1619565, 2396625, 3212885, 4000236, 5101912, 6109280, 7081825, 8291108, 9289165],
        [75497792, 150995256, 150995256,301990208,301990208,603980416,603980416,1207960832,1207960832,2415921664],
        [43671599,87406023,89192495,174930186,176760864,348496700,357556406,699409321,707865047,1401476157],
        "Basic",
        "Bloom Filter",
        "Graph Size (# Nodes)",
        "Space Consumed (Bytes)",
        "Graph Size vs Total Space Consumed",
        f"space10m.png",
    )