import argparse

import numpy as np
import imageio
from graph import Graph

parser = argparse.ArgumentParser()
parser.add_argument("--source_img")
parser.add_argument("--bl_save_path")
parser.add_argument("--reg_save_path")
parser.add_argument("--cost_threshold", default=100, type=int)
args = parser.parse_args()
REG_IMAGE_SAVE_PATH = args.reg_save_path 
BLOOM_IMAGE_SAVE_PATH = args.bl_save_path 
SOURCE_IMAGE = args.source_img 
COST_THRESHOLD = args.cost_threshold


def image_to_graph(img):
    """
    Returns a single node that represents the top-left most (0,0) graph element. 
    The graph node itself is neighbours with the 3-8 nodes that are immediately surrounding it (UDLR + diagonals), but no more
    The graph nodes are indexed by (i, j) tuples of their positions in the image matrix
    """

    graph = Graph(len(img) * len(img[0]))

    for i in range(len(img)):
        for j in range(len(img[0])):
            source = (i, j)
            source_value = img[i][j]

            if i > 0:
                sink = (i - 1, j)
                graph.add_undirected_edge(
                    source,
                    sink,
                    get_distance_tuple(source_value, img[sink[0]][sink[1]]),
                )

                if j > 0:
                    sink = (i - 1, j - 1)
                    graph.add_undirected_edge(
                        source,
                        sink,
                        get_distance_tuple(source_value, img[sink[0]][sink[1]]),
                    )

                if j < len(img[0]) - 1:
                    sink = (i - 1, j + 1)
                    graph.add_undirected_edge(
                        source,
                        sink,
                        get_distance_tuple(source_value, img[sink[0]][sink[1]]),
                    )

            if i < len(img) - 1:
                sink = (i + 1, j)
                graph.add_undirected_edge(
                    source,
                    sink,
                    get_distance_tuple(source_value, img[sink[0]][sink[1]]),
                )

                if j > 0:
                    sink = (i + 1, j - 1)
                    graph.add_undirected_edge(
                        source,
                        sink,
                        get_distance_tuple(source_value, img[sink[0]][sink[1]]),
                    )

                if j < len(img[0]) - 1:
                    sink = (i + 1, j + 1)
                    graph.add_undirected_edge(
                        source,
                        sink,
                        get_distance_tuple(source_value, img[sink[0]][sink[1]]),
                    )

            if j > 0:
                sink = (i, j - 1)
                graph.add_undirected_edge(
                    source,
                    sink,
                    get_distance_tuple(source_value, img[sink[0]][sink[1]]),
                )

            if j < len(img[0]) - 1:
                sink = (i, j + 1)
                graph.add_undirected_edge(
                    source,
                    sink,
                    get_distance_tuple(source_value, img[sink[0]][sink[1]]),
                )
    print("Graph Generated from Image")
    return graph


def mst_to_labels(starting_node, graph_obj, bit_array, cost_threshold, image_size):
    label = 0
    labels = np.zeros(image_size)
    labels[:] = -1
    graph = graph_obj.graph

    def bfs_label(start_node, curr_label):
        q = [start_node]

        while q:
            next_level = []
            for r, c in q:
                labels[r][c] = curr_label
                neighbours = graph[(r, c)]
                for neighbour in neighbours:
                    cost, idx = neighbours[neighbour]
                    if (
                        cost <= cost_threshold
                        and bit_array[idx]
                        and labels[neighbour[0]][neighbour[1]] == -1
                    ):
                        next_level.append(neighbour)

            q = next_level

    for i in range(image_size[0]):
        for j in range(image_size[1]):
            if labels[i][j] == -1:
                bfs_label((i, j), label)
                label += 1

    return labels


def get_distance_tuple(a, b):
    """
    Returns a single integer that represents the euclidean distance between 2 tuple values
    """
    distance = np.sum((np.array(a) - np.array(b)) ** 2)
    return distance


if __name__ == "__main__":
    colours = [[255, 255, 255], [122, 122, 122], [255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 0, 0]]

    img = imageio.imread(SOURCE_IMAGE)
    print("Image Loaded")

    g = image_to_graph(img)
    print(g.n_edges, img.shape)
    cost, _, bit_array = Graph.minimum_spanning_tree(g, (0, 0), True)
    cost_bloom, _, bloom_bit_array, space_total = Graph.bloom_minimum_spanning_tree(g, (0, 0), True)
    labels = mst_to_labels((0, 0), g, bit_array, COST_THRESHOLD, (len(img), len(img[0])))
    bloom_labels = mst_to_labels(
        (0, 0), g, bloom_bit_array, COST_THRESHOLD, (len(img), len(img[0]))
    )

    final_image = np.zeros(img.shape)
    final_bloom = np.zeros(img.shape)

    for i in range(len(final_image)):
        for j in range(len(final_image[0])):
            final_image[i][j] = colours[int(labels[i][j]) % len(colours)]
            final_bloom[i][j] = colours[int(bloom_labels[i][j]) % len(colours)]

    # imageio.imsave(REG_IMAGE_SAVE_PATH, final_image)
    # imageio.imsave(BLOOM_IMAGE_SAVE_PATH, final_bloom)
    imageio.imsave(REG_IMAGE_SAVE_PATH, labels)
    imageio.imsave(BLOOM_IMAGE_SAVE_PATH, bloom_labels)
    print("Images Saved")

