import cv2
import numpy as np
import os
import imutils
from urllib.request import urlopen
from face_ult.captured_face import CapturedFace
from imutils import face_utils
import dlib

class ImgTool:
    BLOCK_THICK = 2
    TEXT_SIZE = 0.75
    color_map = {
        'red': (0, 0, 255),
        'green': (0, 255, 0),
        'blue': (255, 0, 0),
        'pink': (255, 223, 220),
        'tiff_blue': (208, 216, 129)
    }

    @staticmethod
    def get_color(x) -> tuple:
        if isinstance(x, str):
            return ImgTool.color_map[x]
        elif isinstance(x, tuple):
            return x
        else:
            return ImgTool.color_map['red']

    @staticmethod
    def get_rgb_img(img: np.ndarray) -> np.ndarray:
        try:
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"[WARN] {__name__} ♦ failed to convert image color to rgb. Error: {e}")

    @staticmethod
    def resize(img: np.ndarray, size: int) -> np.ndarray:
        return imutils.resize(img, size, size)

    @staticmethod
    def read_img(img_path: str) -> np.ndarray:
        if os.path.exists(img_path):
            try:
                return cv2.imread(img_path)
            except Exception as e:
                print(f"[WARN] {__name__} ♦ failed to read image from path: {img_path} | Error: {e}")

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

    @staticmethod
    def get_rotate_img(image: np.ndarray, angle: float, center=None, scale=1.0) -> np.ndarray:
        temp = image.copy()
        h, w = temp.shape[:2]
        if center is None:
            center = (w / 2, h / 2)
        # rotate
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(temp, M, (w, h))

        return rotated

    @staticmethod
    def get_dnn_blob(img: np.ndarray, proc_size=96, swapRB=True, crop=False):
        try:
            return cv2.dnn.blobFromImage(img, 1.0 / 255, (proc_size, proc_size),
                                         (0, 0, 0), swapRB=swapRB, crop=crop)
        except Exception as e:
            print(f"[WARN] {__name__} ♦ failed to get image blob via cv2.dnn. Error: {e}")

    @staticmethod
    def add_face_block(img: np.ndarray, face_loc, color='green', thick=BLOCK_THICK) -> np.ndarray:
        color = ImgTool.get_color(color)
        if isinstance(face_loc, CapturedFace):
            for face_block in face_loc:
                x, y, w, h = face_utils.rect_to_bb(face_block)
                cv2.rectangle(img, (x, y), (x + w, y + h), color, thick)
        elif isinstance(face_loc, dlib.rectangle):
            x, y, w, h = face_utils.rect_to_bb(face_loc)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, thick)
        return img