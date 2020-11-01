import matplotlib.pyplot as plt
import time
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

    def cost_size_compare(self, start=1000, end=51000, interval=5000):
        # Index of all of these corresponds to the relative graph size (i.e. x[0] is the result for mst(graph(start)))
        graph_size = []
        basic_prims_space = []
        basic_prims_cost = []
        bloom_prims_space = []
        bloom_prims_cost = []
        bloom_prims_stats = []

        for i in range(start, end + 1, interval):
            graph_size.append(i)
            graph = Graph(i).graph
            _, basic_cost, space = Graph.minimum_spanning_tree(graph, "A")
            _, bloom_cost, bloom_stats = Graph.bloom_minimum_spanning_tree(graph, "A")

            basic_prims_space.append(space)
            basic_prims_cost.append(basic_cost)

            bloom_prims_space.append(bloom_stats["space"])
            bloom_prims_cost.append(bloom_cost)
            bloom_prims_stats.append(bloom_stats)

        return (
            graph_size,
            basic_prims_space,
            basic_prims_cost,
            bloom_prims_space,
            bloom_prims_cost,
            bloom_prims_stats,
        )


class ChartGenerator:
    def __init__(self, image_path):
        self.metric_runner = MetricRunner()
        self.image_path = image_path
        self.data = {}

    def get_data(self):
        (
            g_size,
            ba_space,
            ba_cost,
            bl_space,
            bl_cost,
            bl_stats,
        ) = self.metric_runner.cost_size_compare()

        self.data["g_size"] = g_size
        self.data["ba_space"] = ba_space
        self.data["ba_cost"] = ba_cost
        self.data["bl_space"] = bl_space
        self.data["bl_cost"] = bl_cost
        self.data["bl_stats"] = bl_stats

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
            "cost.png",
        )

    def plot_cost_difference(self):
        pass

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
            "space.png",
        )

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
    plotter.get_data()
    plotter.plot_space()
    plotter.plot_costs()
