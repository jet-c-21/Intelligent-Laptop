# coding: utf-8

import dlib
import numpy as np

from face_ult.captured_face import CapturedFace


class FaceCapture:
    dlib_detector = dlib.get_frontal_face_detector()

    @staticmethod
    def cap(img: np.ndarray, mode=None) -> CapturedFace:
        """
        the default detector is dlib detector
        :param img:  numpy.ndarray
        :param mode: str
        :return: FaceBlock
        """
        capt_face = CapturedFace()
        capt_face.detector_type = 'dlib'
        try:
            detect_result = FaceCapture.dlib_detector(img, 1)
        except Exception as e:
            print(e)
            return capt_face

        if len(detect_result):
            capt_face.has_face = True
            capt_face.face_count = len(detect_result)
            capt_face.face_list = detect_result
        else:
            capt_face.has_face = False

        return capt_face
