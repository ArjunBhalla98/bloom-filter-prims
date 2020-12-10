import matplotlib.pyplot as plt
import time
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

    def cost_size_compare(self, start=1000, end=101000, interval=10000, map_edges=False):
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

        for i in range(start, end + 1, interval):
            graph_size.append(i)
            graph_obj = Graph(i)
            graph = graph_obj.graph

            if not map_edges:
                basic_cost, space = Graph.minimum_spanning_tree(graph, "A")
                bloom_cost, bloom_stats = Graph.bloom_minimum_spanning_tree(graph, "A")
            else:
                basic_cost, space, basic_edges = Graph.minimum_spanning_tree(
                    graph, "A", True
                )
                (
                    bloom_cost,
                    bloom_stats,
                    bloom_edges,
                ) = Graph.bloom_minimum_spanning_tree(graph, "A", True)
                bloom_stats["space"] += sys.getsizeof(bloom_edges)
                edge_diff.append(abs(basic_edges.count() - bloom_edges.count()))
                total_edges.append(basic_edges.count())

            basic_prims_space.append(space)
            basic_prims_cost.append(basic_cost)

            bloom_prims_space.append(bloom_stats["space"])
            bloom_prims_cost.append(bloom_cost)
            bloom_prims_stats.append(bloom_stats)

        if not map_edges:
            return (
                graph_size,
                basic_prims_space,
                basic_prims_cost,
                bloom_prims_space,
                bloom_prims_cost,
                bloom_prims_stats,
            )
        else:
            return (
                graph_size,
                basic_prims_space,
                basic_prims_cost,
                bloom_prims_space,
                bloom_prims_cost,
                bloom_prims_stats,
                edge_diff,
                total_edges,
            )


class ChartGenerator:
    def __init__(self, image_path):
        self.metric_runner = MetricRunner()
        self.image_path = image_path
        self.data = {}

    def get_data(self, map_edges=False):
        if not map_edges:
            (
                g_size,
                ba_space,
                ba_cost,
                bl_space,
                bl_cost,
                bl_stats,
            ) = self.metric_runner.cost_size_compare()
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
            ) = self.metric_runner.cost_size_compare(map_edges=True)
            self.data["edge_diff"] = edge_diff
            self.data["n_edges"] = total_edges

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
            f"edges{self.data['g_size'][-1]//1000}k.png",
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
            f"space{self.data['g_size'][-1]//1000}k.png",
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
        plt.plot(x, y1, color="r", marker=".", label=y1_label)
        plt.plot(x, y2, color="b", marker=".", label=y2_label)
        plt.title(title)
        plt.xlabel(x_ax_label)
        plt.ylabel(y_ax_label)
        plt.legend()
        plt.savefig(self.image_path + filename)
        plt.clf()
        print(self.data["bl_stats"])


if __name__ == "__main__":
    plotter = ChartGenerator("./results/")
    plotter.get_data(map_edges=True)
    plotter.plot_space()
    plotter.plot_edge_diff()
    # plotter.plot_costs()
