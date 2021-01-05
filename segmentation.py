import sklearn
import numpy as np
import imageio
import random
import matplotlib.pyplot as plt
from mst_clustering import MSTClustering
from scipy import ndimage

TEST_FILE_SAVE_PATH = "./results/images/test.jpg"
HORSE_IMAGE = "./images/BSDS300/images/test/291000.jpg"

"""
Next steps:

1. Instead of having all the points connected to each other, they should only be connected to their (max 8) direct neighbours
2. implement a full scale / try to scale this up without segfault to BSDS image sets
"""


def image_to_matrix(image):
    """
    Returns a hxwx3 tensor of the given image
    """

    return


if __name__ == "__main__":
    img = imageio.imread(HORSE_IMAGE)
    print("Image Loaded")
    # img = np.mean(img, 2)
    img = img[201:, 321:, :]

    a = len(img)
    b = len(img[0])
    img = np.reshape(img, (len(img) * len(img[0]), 3))
    print("Image reshaped")
    model = sklearn
    model = MSTClustering(cutoff_scale=4.3, approximate=False)
    print("Model init")
    labels = model.fit_predict(img)
    print("Labelled")

    colours = [[255, 255, 255], [0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255]]

    for i in range(len(img)):
        img[i] = colours[labels[i] % len(colours)]

    img = np.reshape(img, (a, b, 3))

    # print(labels)
    imageio.imsave(TEST_FILE_SAVE_PATH, img)
    # print("Image Saved")

