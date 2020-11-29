import numpy as np
import dlib
from face_ult.img_tool import ImgTool
from face_ult.face_capture import FaceCapture
from face_ult.model_api import ModelAPI


class FaceRotate:
    LEFT_EYE_LMK_POS = [36, 37, 38, 39, 40, 41]
    RIGHT_EYE_LMK_POS = [42, 43, 44, 45, 46, 47]

    @staticmethod
    def get_angle_to_hrzl(p1: tuple, p2: tuple):
        deltaY = p1[1] - p2[1]
        deltaX = p1[0] - p2[0]
        return np.arctan(deltaY / deltaX) * 180 / np.pi

    @staticmethod
    def rect_to_tuple(rect):
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        return left, top, right, bottom

    @staticmethod
    def extract_eye(shape, eye_indices):
        points = map(lambda i: shape.part(i), eye_indices)
        return list(points)

    @staticmethod
    def extract_eye_center(shape, eye_indices):
        points = FaceRotate.extract_eye(shape, eye_indices)
        xs = map(lambda p: p.x, points)
        ys = map(lambda p: p.y, points)
        return sum(xs) // 6, sum(ys) // 6

    @staticmethod
    def get_left_eye_center(land_marks):
        return FaceRotate.extract_eye_center(land_marks, FaceRotate.LEFT_EYE_LMK_POS)

    @staticmethod
    def get_right_eye_center(land_marks):
        return FaceRotate.extract_eye_center(land_marks, FaceRotate.RIGHT_EYE_LMK_POS)

    @staticmethod
    def get_landmarks(detector: dlib.shape_predictor, img: np.ndarray, face_block: dlib.rectangle):
        try:
            return detector(img, face_block)
        except Exception as e:
            print(f"failed to detect landmarks from face.  Error: {e}")

    @staticmethod
    def get_rotated_face(img: np.ndarray) -> np.ndarray:
        img = img.copy()
        capt_faces = FaceCapture.cap(img)
        if capt_faces.face_count == 1:
            face_block = capt_faces[0]
            lmk_detector = ModelAPI.get('dlib-lmk68')
            landmark = FaceRotate.get_landmarks(lmk_detector, img, face_block)
            if landmark:
                left_eye_coord = FaceRotate.get_left_eye_center(landmark)
                right_eye_coord = FaceRotate.get_right_eye_center(landmark)
                angle_to_hrzl = FaceRotate.get_angle_to_hrzl(left_eye_coord, right_eye_coord)
                return ImgTool.get_rotate_img(img, angle_to_hrzl)
