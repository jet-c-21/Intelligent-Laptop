import cv2
import numpy as np


class ImgTool:
    @staticmethod
    def get_clarity_val(img: np.ndarray) -> int:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return int(cv2.Laplacian(gray, cv2.CV_64F).var())
