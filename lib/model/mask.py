import numpy as np


def generate_mask(box, img_size):
    """
    Generate a binary bounding box mask

    :param box: (x1, y1, width, height)
    :param img_size: (height, width)
    :return:
    """
    box = box.astype(int)
    box[box < 0] = 0
    x1, y1, w, h = box
    x2, y2 = [x1 + w, y1 + h]
    mask = np.zeros(img_size, dtype=np.uint8)

    if x1 > x2:
        x1, x2 = x2, x1

    if y1 > y2:
        y1, y2 = y2, y1

    mask[y1:y2, x1:x2] = 255

    return mask
