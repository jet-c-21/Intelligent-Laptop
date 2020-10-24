# coding : utf-8
import os
import pandas as pd
from imutils.video import VideoStream
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
        if os.path.exists(RecordMD.meta_path):
            pd.read_csv(RecordMD.meta_path)
        else:
            self.__img_meta = pd.DataFrame(columns=RecordMD.meta_cols)

    def launch(self):
        flag = True
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        fetch_face = 0
        last_face_ts = 0
        while flag:
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            capt_faces = FaceCapture.cap(frame)
            if capt_faces.has_face and capt_faces.face_count == 1:
                ts = FileTool.get_curr_ts()
                if ts - last_face_ts > RecordMD.interval:
                    self.record_face(frame, capt_faces, ts)
                    fetch_face += 1
                    print(f'fetch face successfully. ({fetch_face}/{RecordMD.fetch_count})')
                    last_face_ts = ts

            cv2.imshow("Frame", frame)
            cv2.waitKey(1) & 0xFF

        self.__img_meta.to_csv(RecordMD.meta_path, index=False, encoding='utf-8')
        print('finish saving img meta.')

    def record_face(self, img: np.ndarray, capt_faces: CapturedFace, ts: int):
        face_block = capt_faces[0]
        cropped_face = Cropper.get_cropped_face(img, face_block)

        img_name = f'master_{ts}.jpg'
        img_path = f'{RecordMD.img_dir}/{img_name}'

        date = FileTool.get_date(ts)
        cv2.imwrite(img_path, cropped_face)

        record = [img_name, ts, date.year, date.month, date.day, img_path]
        self.__img_meta.loc[len(record)] = record

