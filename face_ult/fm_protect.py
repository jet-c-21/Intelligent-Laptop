import json
import pathlib
import time
from typing import Union

import cv2
import dlib
import imutils
import numpy as np
from imutils.video import WebcamVideoStream

from face_ult.cropper import Cropper
from face_ult.face_capture import FaceCapture
from face_ult.face_rotate import FaceRotate
from face_ult.faces_proc import FacesProc
from face_ult.img_tool import ImgTool
from face_ult.model_api import ModelAPI
from face_ult.recog_tool import RecogTool
from ult.mail_tool import MailTool
from ult.ui_tool import UITool


class FMProtect:
    DEVICE_DATA_DIR = f"{pathlib.Path(__file__).parent.parent}/DeviceData"
    MASTER_DATA_PATH = f"{DEVICE_DATA_DIR}/master/master.json"
    COMPARE_COUNT = 50
    THRESH_RATE = 0.7

    def __init__(self, mode='custom', display=True):
        # fr-dlib
        self.strangers = None
        self.mode = mode
        self.display = display
        self.model = ModelAPI.get(self.mode)

        self.thresh = None
        self.alert = False

        self.master_info = json.load(open(FMProtect.MASTER_DATA_PATH))
        self.master_name = self.master_info['name']
        self.master_email = self.master_info['email']

    def launch(self):
        self.open_camera()
        self.send_alert()

    def open_camera(self):
        UITool.msg_window('Info', 'Start face model protect mode.')
        flag = True
        vs = WebcamVideoStream(src=0)
        vs.start()
        time.sleep(2.0)
        cv2.startWindowThread()
        while flag:
            frame = vs.read()
            frame = imutils.resize(frame, width=600)
            display_frame = frame.copy()
            capt_faces = FaceCapture.cap(frame)
            if capt_faces.has_face:
                display_frame = ImgTool.add_face_block(display_frame, capt_faces)
                face_data = self.check_faces(frame, capt_faces)
                if face_data:
                    check = self.check_face_encode(face_data)
                    if not check:
                        print(f" WARN - find stranger and no master in the same time !!!")
                        self.alert = True
                else:
                    print('fetched face data is not enough')

            if self.display:
                cv2.imshow('Frame', cv2.flip(display_frame, 1))

            key = cv2.waitKey(1)
            if self.alert or key == 27 or key == ord('q'):
                flag = False
                cv2.waitKey(500)
                cv2.destroyAllWindows()
                cv2.waitKey(500)

        vs.stop()
        cv2.destroyAllWindows()

    def check_faces(self, frame, capt_faces):
        result = list()
        for face_block in capt_faces:
            face_data = self.face_pipeline(frame, face_block)
            if face_data is not False:
                result.append(face_data)
        return result

    def face_pipeline(self, img, face_block: dlib.rectangle) -> Union[tuple, bool]:
        cropped_face = Cropper.get_smart_cropped_face(img, face_block)
        if not FacesProc.is_single_face(cropped_face):
            print('the cropped face is not single.')
            return False

        if not FacesProc.is_clear(cropped_face):
            print('the cropped face is too blurry.')
            return False

        rotated_face = FaceRotate.get_rotated_face(cropped_face)
        if rotated_face is None:
            print('failed to rotate face')
            return False

        embed = RecogTool.get_face_embed(rotated_face)
        if embed is None:
            print('failed to get embed')
            return False

        return embed, rotated_face

    def check_face_encode(self, face_data: list) -> bool:
        print('checking faces...')
        strangers = list()
        has_master = False
        for d in face_data:
            face_encode = d[0]
            if self.is_master(face_encode):
                print('hi master !!!')
                has_master = True
            else:
                print('[INFO] - find stranger')
                portrait = d[1]
                strangers.append(portrait)

        if len(strangers) and not has_master:
            self.strangers = strangers
            return False
        else:
            return True

    def is_master(self, face_encode: np.ndarray):
        predict = self.model.predict([face_encode])
        if predict[0] == 1:
            return True
        else:
            return False

    def send_alert(self):
        if self.alert:
            mt = MailTool(self.master_name, self.master_email)
            mt.send_notification(self.strangers)
