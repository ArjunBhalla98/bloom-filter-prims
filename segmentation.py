import mst_clustering
import sklearn
import numpy as np
import imageio
import random
from scipy import ndimage

TEST_FILE_SAVE_PATH = "./results/images/test.jpg"
HORSE_IMAGE = "./images/BSDS300/images/test/291000.jpg"


def image_to_matrix(image):
    """
    Returns a hxwx3 tensor of the given image
    """

    return


if __name__ == "__main__":
    img = imageio.imread(HORSE_IMAGE)
    print("Image Loaded")
    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j][0] = random.randint(0, 255)

    imageio.imsave(TEST_FILE_SAVE_PATH, img)
    print("Image Saved")

