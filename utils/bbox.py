import numpy as np


def get_center_of_bbox(bbox):
    x1, y1, x2, y2 = bbox
    x_center = (x1 + x2) // 2
    y_center = (y1 + y2) // 2
    return np.array([x_center, y_center])


def get_center_of_legs(bbox):
    x1, y1, x2, y2 = bbox
    x_center = (x1 + x2) // 2
    return np.array([x_center, y2])


def get_area(bbox):
    if bbox is None:
        return 0
    x1, y1, x2, y2 = bbox
    height = y2 - y1
    width = x2 - x1
    area = height * width
    return area
