import cv2
import numpy as np
import sys

sys.path.append("../")
from utils import get_distance_from_line, get_line_from_points, get_center_of_legs


class CreatureDetector:
    def __init__(self, transformer):
        # Hardcoded parameter
        self.points = [(1468, 2044), (1468, 2466)]

        # Trabajamos en el espacio transformado utilizando coordenadas homogeneas
        self.transformer = transformer
        self.line = get_line_from_points(self.points[0], self.points[1])

    def get_creature_distance(self, bbox):
        """Dado un segmento vertical, calcula la distancia de la linea
        a la criatura, siempre y cuando la criatura este entre los limites
        de la linea
        """
        if bbox is None:
            return None
        foot = get_center_of_legs(bbox)
        foot = self.transformer.warp_point(foot)
        # Revisar si esta entre las lineas
        line_start = self.points[0][1]
        line_end = self.points[1][1]
        y_foot = foot[1]
        if y_foot > line_start and y_foot < line_end:
            distance = get_distance_from_line(self.line, foot)
        else:
            distance = None
        return distance

    def draw_frame(self, frame, bbox):
        distance = self.get_creature_distance(bbox)
        frame = self.draw_line(frame)
        frame = self.draw_bbox(frame, bbox, distance)
        return frame

    def draw_line(self, frame):
        line_start = np.array(self.points[0])
        line_end = np.array(self.points[1])
        # Unwarp line
        line_start = self.transformer.unwarp_point(line_start)
        line_start = line_start.astype("int")
        line_end = self.transformer.unwarp_point(line_end)
        line_end = line_end.astype("int")
        frame = cv2.line(frame, line_start, line_end, (0, 0, 0), 3)
        return frame

    def draw_bbox(self, frame, bbox, distance):
        # myframe = frame.copy()
        # cv2.rectangle(myframe, ())
        if bbox is not None:
            frame = cv2.rectangle(frame, bbox[0:2], bbox[2:], (0, 0, 255), 2)
            if distance is not None:
                # foot = get_center_of_legs(bbox)
                foot = bbox[0], bbox[3]
                frame = cv2.putText(
                    frame,
                    f"Distancia: {distance:.0f}",
                    (foot[0], foot[1] + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1,
                )
        return frame
