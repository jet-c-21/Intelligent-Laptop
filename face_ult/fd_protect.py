import json
import pathlib
import random
import time

import cv2
import face_recognition
import imutils
import numpy as np
from imutils import paths
from imutils.video import WebcamVideoStream
from tqdm import tqdm

from face_ult.face_capture import FaceCapture
from face_ult.faces_proc import FacesProc
from face_ult.img_tool import ImgTool
from ult.mail_tool import MailTool
from ult.ui_tool import UITool


class FDProtect:
    DEVICE_DATA_DIR = f"{pathlib.Path(__file__).parent.parent}/DeviceData"
    MASTER_DATA_PATH = f"{DEVICE_DATA_DIR}/master/master.json"
    COMPARE_COUNT = 50
    THRESH_RATE = 0.7

    def __init__(self, mode='fr-dlib', display=True):
        self.mode = mode
        self.display = display
        # fr-dlib
        self.strangers = None
        self.compare_count = FDProtect.COMPARE_COUNT
        self.master_data = list()
        self.thresh = None
        self.alert = False

        self.master_info = json.load(open(FDProtect.MASTER_DATA_PATH))
        self.master_name = self.master_info['name']
        self.master_email = self.master_info['email']

    def _load_master_data(self):
        img_paths = list(paths.list_images(FDProtect.DEVICE_DATA_DIR))
        random.shuffle(img_paths)
        for p in tqdm(img_paths):
            image = ImgTool.read_img(p)
            if image is not None:
                # face_encode = FacesProc.get_face_encode_from_raw(self.mode, image)
                face_data = FacesProc.get_all_faces_with_encode(image, self.mode)
                if face_data:
                    self.master_data.append(face_data[0]['encode'])

            if len(self.master_data) >= self.compare_count:
                break

        # type_check = set()
        # for m in self.master_data:
        #     type_check.add(type(m))
        # print(type_check)

        self.thresh = int(len(self.master_data) * FDProtect.THRESH_RATE)

    def launch(self):
        print('loading master data...')
        self._load_master_data()
        print(f"finish loading master data. thresh: {self.thresh}")
        self.open_camera()
        self.send_alert()

    def open_camera(self):
        UITool.msg_window('Info', 'Start face distant protect mode.')
        flag = True
        vs = WebcamVideoStream(src=0)
        vs.start()
        time.sleep(2.0)
        cv2.startWindowThread()
        while flag:
            check = True
            frame = vs.read()
            frame = imutils.resize(frame, width=800)
            display_frame = frame.copy()
            capt_faces = FaceCapture.cap(frame)
            if capt_faces.has_face:
                display_frame = ImgTool.add_face_block(display_frame, capt_faces)
                face_data = FacesProc.get_all_faces_with_encode_low_filter(frame, self.mode)
                if face_data:
                    check = self.check_face_encode(face_data)
                    print(f"status: {check}")
                    if not check:
                        print(f" WARN - find stranger and no master in the same time !!!")
                        self.alert = True
                else:
                    print('fetched face data is not enough')

            if self.display:
                display_frame = cv2.flip(display_frame, 1)
                if check:
                    text = 'Safe'
                    print(text)
                    display_frame = ImgTool.add_text(display_frame, text)
                else:
                    text = 'Detect Stranger!'
                    display_frame = ImgTool.add_text(display_frame, text, color='red')

                cv2.imshow('Frame', display_frame)

            key = cv2.waitKey(1)
            if self.alert or key == 27 or key == ord('q'):
                flag = False
                cv2.waitKey(500)
                cv2.destroyAllWindows()
                cv2.waitKey(500)

        vs.stop()
        cv2.destroyAllWindows()

    def check_face_encode(self, face_data: list) -> bool:
        print('checking faces...')
        strangers = list()
        has_master = False
        for d in face_data:
            face_encode = d['encode']
            if self.is_master(face_encode):
                has_master = True
            else:
                print('[INFO] - find stranger')
                portrait = d['portrait']
                strangers.append(portrait)

        if len(strangers) and not has_master:
            self.strangers = strangers
            return False
        else:
            return True

    def is_master(self, face_encode: np.ndarray):
        matches = face_recognition.compare_faces(self.master_data, face_encode)
        score = np.sum(matches)
        print(f"score: {score}  thresh: {self.thresh}")
        if score >= self.thresh:
            return True
        else:
            return False

    def send_alert(self):
        if self.alert:
            mt = MailTool(self.master_name, self.master_email)
            mt.send_notification(self.strangers)

    def test(self, img):
        face_data = FacesProc.get_all_faces_with_encode(img, self.mode)
        check = self.check_face_encode(face_data)
        print(f"status: {check}")
        if not check:
            print(f" WARN - find stranger !!!")
            self.alert = True
