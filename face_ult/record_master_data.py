# coding : utf-8
import os
import time

import cv2
import imutils
import numpy as np
import pandas as pd
from imutils.video import WebcamVideoStream

from face_ult.cropper import Cropper
from face_ult.face_capture import FaceCapture, CapturedFace
from face_ult.face_rotate import FaceRotate
from face_ult.faces_proc import FacesProc
from face_ult.img_tool import ImgTool
from face_ult.recog_tool import RecogTool
from ult.file_tool import FileTool
from ult.ui_tool import UITool


class RecordMD:
    IMG_DIR = 'DeviceData/master/img'
    META_PATH = 'DeviceData/master/img_meta.csv'  # deprecate
    META_COLS = ['id', 'ts', 'year', 'month', 'day', 'clarity', 'img_path']  # deprecate

    INTERVAL = 1
    DISPLAY_SIZE = 500

    def __init__(self, fetch_count=2, display=True):
        self.fetch_count = fetch_count
        self.display = display
        self.__img_meta: pd.DataFrame
        if not os.path.exists(RecordMD.IMG_DIR):
            os.mkdir(RecordMD.IMG_DIR)

        if os.path.exists(RecordMD.META_PATH):
            self.__img_meta = pd.read_csv(RecordMD.META_PATH)
        else:
            self.__img_meta = pd.DataFrame(columns=RecordMD.META_COLS)

    def launch(self):
        flag = True
        vs = WebcamVideoStream(src=0)
        vs.start()
        time.sleep(2.0)
        fetch_face = 0
        last_face_ts = 0
        cv2.startWindowThread()
        while flag:
            frame = vs.read()
            if frame is None:
                continue
            frame = imutils.resize(frame, width=800)
            display_frame = frame.copy()
            capt_faces = FaceCapture.cap(frame)
            if capt_faces.face_count == 1:
                display_frame = ImgTool.add_face_block(display_frame, capt_faces)
                ts = FileTool.get_curr_ts()
                if ts - last_face_ts > RecordMD.INTERVAL:
                    if self.__record_face(frame, capt_faces, ts):
                        fetch_face += 1
                        print(f'fetch face successfully. ({fetch_face}/{self.fetch_count})')
                        last_face_ts = ts
                    else:
                        print(f'failed to record faces')

            if self.display:
                display_frame = cv2.flip(display_frame, 1)
                text = f"{fetch_face} / {self.fetch_count}"
                display_frame = ImgTool.add_text(display_frame, text)
                cv2.imshow('Frame', display_frame)

            key = cv2.waitKey(1)

            if fetch_face == self.fetch_count or key == 27 or key == ord('q'):
                flag = False
                cv2.waitKey(500)
                cv2.destroyAllWindows()
                cv2.waitKey(500)

        vs.stop()
        cv2.destroyAllWindows()

        # self.__img_meta.to_csv(RecordMD.meta_path, index=False, encoding='utf-8')
        msg = 'Finish recoding master data.'
        UITool.msg_window(msg=msg)

        print('finish saving img meta.')

    def __record_face(self, img: np.ndarray, capt_faces: CapturedFace, ts: int) -> bool:
        face_block = capt_faces[0]
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

        if RecogTool.can_get_embed(rotated_face, 'cv2-dnn'):
            # save the face image
            img_name = f'master_{ts}.jpg'
            img_path = f'{RecordMD.IMG_DIR}/{img_name}'
            # date = FileTool.get_date(ts)
            cv2.imwrite(img_path, cropped_face)
            return True

            # save record in metadata
            # record = [img_name, ts, date.year, date.month, date.day, face_clarity, img_path]
            # self.__img_meta.loc[len(self.__img_meta)] = record
