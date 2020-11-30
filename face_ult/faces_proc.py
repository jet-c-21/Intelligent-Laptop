import numpy as np
import dlib
from face_ult.face_capture import FaceCapture
from face_ult.cropper import Cropper
from face_ult.img_tool import ImgTool
from face_ult.face_rotate import FaceRotate
from face_ult.model_api import ModelAPI
from typing import Union
import face_recognition


class FacesProc:
    CLARITY_THRESH = 50

    @staticmethod
    def dlib_rect_to_boxes(rect: dlib.rectangle) -> tuple:
        return rect.top(), rect.right(), rect.bottom(), rect.left()

    @staticmethod
    def is_clear(img: np.ndarray) -> bool:
        clarity_val = ImgTool.get_clarity_val(img)
        if clarity_val >= FacesProc.CLARITY_THRESH:
            return True
        else:
            return False

    @staticmethod
    def is_single_face(img: np.ndarray) -> bool:
        if FaceCapture.cap(img).face_count == 1:
            return True
        else:
            return False

    @staticmethod
    def get_portrait(img: np.ndarray, face_block: dlib.rectangle) -> Union[np.ndarray, None]:
        if not FacesProc.is_clear(img):
            return

        cropped_face = Cropper.get_smart_cropped_face(img, face_block)
        if not FacesProc.is_single_face(cropped_face):
            return

        rotated_face = FaceRotate.get_rotated_face(cropped_face)
        if not FacesProc.is_single_face(rotated_face):
            return

        return rotated_face

        # return img

    @staticmethod
    def get_face_grid(img: np.ndarray) -> np.ndarray:
        capt_faces = FaceCapture.cap(img)
        if capt_faces.has_face:
            face_block = capt_faces[0]
            return Cropper.get_cropped_face(img, face_block, 0)

    @staticmethod
    def get_face_encode(img: np.ndarray, mode: str, proc_size=96) -> Union[np.ndarray, None]:
        """
        1. cv2-dnn
        2. fr-dlib

        :param img:
        :param mode:
        :param proc_size:
        :return:
        """
        if mode == 'cv2-dnn':
            embed_model = ModelAPI.get('openface-embed')
            img = face_recognition.load_image_file(img)
            face_blob = ImgTool.get_dnn_blob(img, proc_size)
            if face_blob is not None:
                embed_model.setInput(face_blob)
                vec = embed_model.forward()
                print(vec)
                return vec.flatten()

        elif mode == 'fr-dlib':
            face = ImgTool.get_rgb_img(img)
            if face is None:
                return

            face = ImgTool.resize(face, proc_size)
            if face is None:
                return

            capt_faces = FaceCapture.cap(face)
            if capt_faces.face_count != 1:
                return

            fb = capt_faces[0]
            box = FacesProc.dlib_rect_to_boxes(fb)
            result = face_recognition.face_encodings(face, [box])
            if len(result):
                return result[0]

    @staticmethod
    def get_face_encode_from_raw(mode: str, img: np.ndarray, face_block=None) -> Union[np.ndarray, None]:
        if face_block is not None:
            portrait = FacesProc.get_portrait(img, face_block)
            if portrait is None:
                return

            face_grid = FacesProc.get_face_grid(portrait)
            if face_grid is None:
                return

            return FacesProc.get_face_encode(face_grid, mode)

        else:
            capt_faces = FaceCapture.cap(img)
            if capt_faces.face_count != 1:
                return
            face_block = capt_faces[0]
            return FacesProc.get_face_encode_from_raw(mode, img, face_block)

    @staticmethod
    def get_encodes_of_faces_in_frame(img: np.ndarray, mode: str) -> list:
        result = list()
        capt_faces = FaceCapture.cap(img)
        for face_block in capt_faces:
            face_encode = FacesProc.get_face_encode_from_raw(mode, img, face_block)
            if face_encode is not None:
                result.append(face_encode)

        return result

    @staticmethod
    def get_all_faces_with_encode(img: np.ndarray, mode: str) -> list:
        result = list()
        capt_faces = FaceCapture.cap(img)
        for face_block in capt_faces:
            portrait = FacesProc.get_portrait(img, face_block)
            if portrait is None:
                print('failed to get portrait from image')
                continue

            face_grid = FacesProc.get_face_grid(portrait)
            if face_grid is None:
                print('failed to get face grid from image')
                continue

            face_encode = FacesProc.get_face_encode(img, mode)
            if face_encode is not None:
                record = {'portrait': portrait, 'encode': face_encode}
                result.append(record)
            else:
                print('failed to get face encode from image')

        return result

    @staticmethod
    def get_all_faces_with_encode_low_filter(img: np.ndarray, mode: str) -> list:
        result = list()
        capt_faces = FaceCapture.cap(img)
        for face_block in capt_faces:
            cropped_face = Cropper.get_smart_cropped_face(img, face_block)
            face_grid = FacesProc.get_face_grid(cropped_face)
            if face_grid is None:
                print('failed to get face grid')
                continue

            face_encode = FacesProc.get_face_encode(img, mode)
            if face_encode is not None:
                record = {'portrait': cropped_face, 'encode': face_encode}
                result.append(record)
            else:
                print('failed to get face encode')

        return result
