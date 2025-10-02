import numpy as np


def transform_coordinates(point):
    """Transforma las coordenadas de un punto desde R2 al espacio RP2"""
    point = np.array([point[0], point[1], 1])
    return point


def get_line_from_points(p1, p2):
    """Entrega los coeficientes en coordenadas homogeneas
    de la linea que pasa por p1 y p2"""
    Points = np.array([p1, p2])
    scale = np.array([-1, -1])
    coefficients = np.linalg.solve(Points, scale)
    norm = np.linalg.norm(coefficients)
    coefficients = coefficients / norm
    c = 1 / norm
    return np.array([coefficients[0], coefficients[1], c])


def get_distance_from_line(line, point):
    """Calcula la distancia entre una linea en coordenadas homogeneas
    y un punto"""
    point = transform_coordinates(point)
    return line @ point