# coding: utf-8
import pathlib

import cv2
import dlib
import numpy


class CapturedFace:
    def __init__(self):
        self.has_face = None
        self.face_count = 0
        self.face_list = list()
        self.detector_type = ''

    def __str__(self):
        text = f'Has Face: {self.has_face}\n'
        text += f'Face Count: {self.face_count}\n'
        text += f'Detector Type: {self.detector_type}\n'
        text += f'Face List:\n'
        for i, f in enumerate(self.face_list, start=1):
            text += f'\t Face-{i}: {str(f)}'
        return text.strip()

    def __getitem__(self, item):
        return self.face_list[item]



class FaceCapture:
    dlib_detector = dlib.get_frontal_face_detector()

    @staticmethod
    def cap(img: numpy.ndarray, mode='default') -> CapturedFace:
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
