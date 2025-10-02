import cv2
import numpy as np


class PerspectiveTransformer:
    def __init__(self):
        # Hardcoded parameters that define transformation
        self.pixel_verticies = np.array(
            [(342, 276), (537, 299), (27, 410), (472, 455)], dtype="float32"
        )
        self.target_verticies = np.array(
            [(0, 0), (272, 0), (0, 500), (500, 500)], dtype="float32"
        )
        # Parameters related to image size
        self.height = 478
        self.width = 770

        # Calculate matrix for transform
        self.H = cv2.getPerspectiveTransform(
            self.pixel_verticies, self.target_verticies
        )
        # Define corners of the image
        corners = np.array(
            [[0, 0], [self.width, 0], [self.width, self.height], [0, self.height]],
            dtype=np.float32,
        )

        # Transform corners using the perspective transformation
        warped_corners = cv2.perspectiveTransform(
            corners.reshape(1, 4, 2), self.H
        ).reshape(4, 2)

        # Extract coordinates of transformed corners
        x = warped_corners[:, 0]
        y = warped_corners[:, 1]

        # Find bounding box of the warped corners
        x0, y0 = np.floor(np.min(x)), np.floor(np.min(y))
        x1, y1 = np.ceil(np.max(x)), np.ceil(np.max(y))
        self.warped_width = int(x1 - x0)
        self.warped_height = int(y1 - y0)

        # Create translation matrix
        T = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]], dtype=np.float32)

        # Created adjusted H and its inverse
        self.H_adjusted = T @ self.H
        self.H_adjusted_inv = np.linalg.inv(self.H_adjusted)

    def warp_point(self, point):
        """Transforma un punto con la matriz H"""
        reshaped_point = point.reshape(-1, 1, 2).astype(np.float32)
        transform_point = cv2.perspectiveTransform(reshaped_point, self.H_adjusted)
        transform_point = transform_point.reshape(2)
        return transform_point

    def unwarp_point(self, point):
        """Transforma un punto con la inversa de la matriz H"""
        reshaped_point = point.reshape(-1, 1, 2).astype(np.float32)
        transform_point = cv2.perspectiveTransform(reshaped_point, self.H_adjusted_inv)
        return transform_point.reshape(2)

    def warp_perspective(self, img):
        """Transformar toda la imagen con la matriz H"""
        # Warp the image
        warped = cv2.warpPerspective(
            img,
            self.H_adjusted,
            (self.warped_width, self.warped_height),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT,
        )
        return warped

    def unwarp_perspective(self, img):
        """Destransformar toda la imagen con la inversa de la matriz H"""
        # Unwarp the image
        unwarped = cv2.warpPerspective(
            img,
            self.H_adjusted_inv,
            (self.width, self.height),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT,
        )
        return unwarped
