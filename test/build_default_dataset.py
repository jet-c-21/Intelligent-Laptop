# coding: utf-8
"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2020/11/28
"""
from face_ult.data_updater import ArtistGenerator, DataUpdater, BingImgAPI
from face_ult.img_tool import ImgTool
from pprint import pprint as pp
import dlib
from face_ult.display_tool import DisplayTool as dt
from face_ult.model_api import ModelAPI
from face_ult.face_capture import FaceCapture
from face_ult.display_tool import DisplayTool as dt
from ult.file_tool import FileTool
import cv2
import numpy as np

from face_ult.cropper import Cropper

artists = ArtistGenerator.get_artist()

MAX = 600

def artist_handler(artist:str):
    data_dir = f"data/{artist}"
    FileTool.create_folder(data_dir)
    done_img = 0

    while done_img >= MAX:
        img_urls = BingImgAPI.get_img_urls('bts')



if __name__ == '__main__':
    # image = cv2.imread('bts.jpg')

    artists = ['BTS', 'Justin Bieber', 'Zedd']

    for artist in artists:
        artist_handler(artist)
        break





