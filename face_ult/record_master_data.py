# coding : utf-8
import os
import pandas as pd
from imutils.video import WebcamVideoStream
import argparse
import imutils
import time
import cv2
import os
import numpy as np

from face_ult.face_capture import FaceCapture, CapturedFace
from face_ult.cropper import Cropper
from ult.file_tool import FileTool


class RecordMD:
    img_dir = 'DeviceData/master/img'
    meta_path = 'DeviceData/master/img_meta.csv'
    meta_cols = ['id', 'ts', 'year', 'month', 'day', 'img_path']
    fetch_count = 10
    interval = 3

    def __init__(self):
        self.__img_meta: pd.DataFrame
        if not os.path.exists(RecordMD.img_dir):
            os.mkdir(RecordMD.img_dir)

        if os.path.exists(RecordMD.meta_path):
            self.__img_meta = pd.read_csv(RecordMD.meta_path)
        else:
            self.__img_meta = pd.DataFrame(columns=RecordMD.meta_cols)

    def launch(self):
        flag = True
        vs = WebcamVideoStream(src=0).start()
        time.sleep(2.0)
        fetch_face = 0
        last_face_ts = 0
        while flag:
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            capt_faces = FaceCapture.cap(frame)
            if self.__check_cap_faces(capt_faces):
                ts = FileTool.get_curr_ts()
                if ts - last_face_ts > RecordMD.interval:
                    if self.__record_face(frame, capt_faces, ts):
                        fetch_face += 1
                        print(f'fetch face successfully. ({fetch_face}/{RecordMD.fetch_count})')
                        last_face_ts = ts
                    else:
                        print(f'failed to record faces')

            cv2.imshow('Frame', frame)
            cv2.waitKey(1) & 0xFF

            if fetch_face == RecordMD.fetch_count:
                flag = False

        self.__img_meta.to_csv(RecordMD.meta_path, index=False, encoding='utf-8')
        print('finish saving img meta.')

    def __record_face(self, img: np.ndarray, capt_faces: CapturedFace, ts: int) -> bool:
        face_block = capt_faces[0]
        cropped_face = Cropper.get_cropped_face(img, face_block, 0.9)
        if self.__check_cap_faces(FaceCapture.cap(cropped_face)):
            img_name = f'master_{ts}.jpg'
            img_path = f'{RecordMD.img_dir}/{img_name}'

            date = FileTool.get_date(ts)
            cv2.imwrite(img_path, cropped_face)

            record = [img_name, ts, date.year, date.month, date.day, img_path]
            self.__img_meta.loc[len(self.__img_meta)] = record
            return True
        else:
            return False

    @staticmethod
    def __check_cap_faces(capt_faces: CapturedFace):
        if capt_faces.has_face and capt_faces.face_count == 1:
            return True
        else:
            return False
