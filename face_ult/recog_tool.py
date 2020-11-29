# coding: utf-8
"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2020/11/15
"""
import cv2
import numpy as np
import face_recognition
import multiprocessing as mp
from functools import partial
from tqdm import tqdm
import imutils

from face_ult.cropper import Cropper
from face_ult.face_capture import FaceCapture
from face_ult.img_tool import ImgTool
from face_ult.model_api import ModelAPI


class RecogTool:
    @staticmethod
    def _get_face_embed(img: np.ndarray, proc_size: int, mode: str) -> np.ndarray:
        capt_faces = FaceCapture.cap(img)
        if not capt_faces.has_face:
            print(f"[WARN] {__name__} ♦ failed to get face-embed cuz FaceCapture can't capture any faces")
            return

        if capt_faces.face_count != 1:
            print(f"[WARN] {__name__} ♦ failed to get face-embed cuz the count of CapturedFace is not 1")
            return

        face = Cropper.get_cropped_face(img, capt_faces[0], 0)

        if mode == 'cv2-dnn':
            embed_model = ModelAPI.get('openface-embed')
            face_blob = ImgTool.get_dnn_blob(img, proc_size)
            if face_blob is not None:
                embed_model.setInput(face_blob)
                vec = embed_model.forward()
                return vec.flatten()

        elif mode == 'fr-dlib':
            face = ImgTool.get_rgb_img(face)
            if face is not None:
                face = ImgTool.resize(face, proc_size)
                return face_recognition.face_encodings(face)[0]

    @staticmethod
    def get_face_embed(img, proc_size=96, mode='cv2-dnn') -> np.ndarray:
        if isinstance(img, str):
            img = ImgTool.read_img(img)
            if img is not None:
                return RecogTool._get_face_embed(img, proc_size, mode)

        elif isinstance(img, np.ndarray):
            return RecogTool._get_face_embed(img, proc_size, mode)

    @staticmethod
    def get_face_embed_sequence(img_paths: list, proc_size=96, mode='cv2-dnn') -> [np.ndarray]:
        with mp.Pool() as pool:
            task = partial(RecogTool.get_face_embed, proc_size=proc_size, mode=mode)
            result = list(
                tqdm(
                    pool.imap(task, img_paths), total=len(img_paths)
                )
            )

        return result

    @staticmethod
    def get_face_embed_labeling(data: list, proc_size=96, mode='cv2-dnn', drop_failed=True) -> list:
        """
        data = [
            [label, img_path]
        ]
        and add face-embed to original data ->  [label, img_path, face_embed]
        :param data:
        :param proc_size:
        :param mode:
        :param drop_failed:
        :return:
        """
        img_paths = [d[1] for d in data]
        face_embeds = RecogTool.get_face_embed_sequence(img_paths, proc_size, mode)

        if drop_failed:
            result = list()
            for d, embed in zip(data, face_embeds):
                if embed is not None:
                    d.append(embed)
                    result.append(d)

            return result

        else:
            for i in range(len(data)):
                embed = face_embeds[i]
                data[i].append(embed)

            return data

    @staticmethod
    def can_get_embed(img: np.ndarray) -> bool:
        try:
            embed = RecogTool.get_face_embed(img)
            if embed is not None:
                return True
        except Exception as e:
            print(f"can't get face embed error: {e}")
            return False
