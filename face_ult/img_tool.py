import cv2
import numpy as np
from urllib.request import urlopen


class ImgTool:
    @staticmethod
    def get_clarity_val(img: np.ndarray) -> int:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return int(cv2.Laplacian(gray, cv2.CV_64F).var())

    @staticmethod
    def url_to_img(url: str) -> np.ndarray:
        try:
            response = urlopen(url)
            image = np.asarray(bytearray(response.read()), dtype="uint8")
            return cv2.imdecode(image, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"failed to convert url to image. url: {url}  Error: {e}")
