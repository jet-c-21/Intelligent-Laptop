# coding: utf-8
import ntpath
import os
import pathlib

import cv2
import dlib
from joblib import load
from sklearn.pipeline import Pipeline


class ModelAPI:
    MODEL_DIR_NAME = 'model'
    MODEL_DIR = pathlib.Path(f"{pathlib.Path(__file__).parent}/{MODEL_DIR_NAME}").absolute()

    @staticmethod
    def _path_convert(path_str: str, path_type: str) -> str:
        if path_type is None:
            return ntpath.abspath(path_str)

        elif path_type == 'win':
            return ntpath.abspath(path_str).replace('/', '\\')

        elif path_type in ['unix', 'linux', 'mac']:
            return ntpath.abspath(path_str).replace('\\', '/')

    @staticmethod
    def _dlib_lmk68_router(path_type) -> str:
        n = 'shape_predictor_68_face_landmarks.dat'
        s = f"{ModelAPI.MODEL_DIR}/official/dlib/{n}"
        return ModelAPI._path_convert(s, path_type)

    @staticmethod
    def _openface_embed_router(path_type) -> str:
        n = 'openface_nn4.small2.v1.t7'
        s = f"{ModelAPI.MODEL_DIR}/official/embed/{n}"
        return ModelAPI._path_convert(s, path_type)

    @staticmethod
    def _custom_router(path_type) -> str:
        d = f"{ModelAPI.MODEL_DIR}/custom"
        temp = list()
        for n in os.listdir(d):
            if n == 'demo.joblib':
                continue
            score = n.split('.')[0]
            temp.append(score)

        if len(temp):
            pick = max(temp)
            s = f"{d}/{pick}.joblib"
            return ModelAPI._path_convert(s, path_type)

    @staticmethod
    def _demo_router(path_type) -> str:
        s = f"{ModelAPI.MODEL_DIR}/custom/demo.joblib"
        return ModelAPI._path_convert(s, path_type)

    @staticmethod
    def get_path(model_name: str, path_type=None) -> str:
        """
        1. dlib-lmk68
        2. openface_embed
        3. custom
        4. demo

        :param path_type: win, mac, unix, linux
        :param model_name:
        :return:
        """

        if model_name == 'dlib-lmk68':
            return ModelAPI._dlib_lmk68_router(path_type)

        elif model_name == 'openface-embed':
            return ModelAPI._openface_embed_router(path_type)

        elif model_name == 'custom':
            return ModelAPI._custom_router(path_type)

        elif model_name == 'demo':
            return ModelAPI._demo_router(path_type)

    @staticmethod
    def get(model_name: str):
        """
        1. dlib-lmk68
        2. openface-embed
        3. custom
        4. demo

        :param model_name:
        :return:
        """
        if model_name == 'dlib-lmk68':
            return ModelAPI._dlib_lmk68_helper()

        elif model_name == 'openface-embed':
            return ModelAPI._openface_embed_helper()

        elif model_name == 'custom':
            return ModelAPI._custom_helper()

        elif model_name == 'demo':
            return ModelAPI._demo_helper()

    @staticmethod
    def _dlib_lmk68_helper() -> dlib.shape_predictor:
        p = ModelAPI._dlib_lmk68_router('linux')
        return dlib.shape_predictor(p)

    @staticmethod
    def _openface_embed_helper() -> dlib.shape_predictor:
        p = ModelAPI._openface_embed_router('linux')
        return cv2.dnn.readNetFromTorch(p)

    @staticmethod
    def _custom_helper() -> Pipeline:
        p = ModelAPI._custom_router('linux')
        if p:
            return load(p)

    @staticmethod
    def _demo_helper() -> Pipeline:
        p = ModelAPI._demo_router('linux')
        return load(p)
