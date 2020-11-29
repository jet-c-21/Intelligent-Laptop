# coding: utf-8
"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2020/11/28
"""
import os
import asyncio
import aiohttp
import requests
import pyquery
import numpy as np
import cv2
import multiprocessing as mp
from pyquery import PyQuery as pq
from ult.file_tool import FileTool
from tqdm import tqdm
from face_ult.face_capture import FaceCapture
from face_ult.cropper import Cropper
from face_ult.face_rotate import FaceRotate
from face_ult.recog_tool import RecogTool
from requests.models import Response
from pprint import pprint as pp


class ArtistGenerator:
    ESC_CHAR = [
        '\\', '/', '*', ':', '*',
        '?', '"', "'", '<', '>',
        '|'
    ]

    @staticmethod
    def _replace(s: str) -> str:
        for c in ArtistGenerator.ESC_CHAR:
            s = s.replace(c, ' ')
        return s

    @staticmethod
    def _access(url) -> pyquery.PyQuery:
        try:
            return pq(requests.get(url).text)
        except Exception as e:
            print(f"[WARN] - failed to get document from url: {url}  Error: {e}")

    @staticmethod
    def _get_billboard_hot100() -> list:
        result = set()
        url = 'https://www.billboard.com/charts/hot-100'
        doc = ArtistGenerator._access(url)
        chart = doc('div.chart-list.container')
        artist_list = chart('span.chart-element__information__artist.text--truncate.color--secondary')

        for el in artist_list.items():
            name = ArtistGenerator._replace(el.text())
            result.add(name)

        return list(result)

    @staticmethod
    def _get_billboard_artist100() -> list:
        result = set()
        url = 'https://www.billboard.com/charts/artist-100'
        doc = ArtistGenerator._access(url)
        chart = doc('div.chart-list.chart-details__left-rail')
        artist_list = chart('span.chart-list-item__title-text > a')

        for el in artist_list.items():
            name = ArtistGenerator._replace(el.text())
            result.add(name)

        return list(result)

    @staticmethod
    def get_artist() -> list:
        result = set()
        result.update(ArtistGenerator._get_billboard_hot100())
        result.update(ArtistGenerator._get_billboard_artist100())
        return sorted(list(result))


class BingImgAPI:
    KEY = 'd7dc63e5f1fd4c7e82f8879604e21a62'
    URL = 'https://api.bing.microsoft.com/v7.0/images/search'
    HEADER = {'Ocp-Apim-Subscription-Key': KEY}

    @staticmethod
    def get_img_urls(q: str, count=150, offset=0, min_size=200, max_size=None) -> dict:
        result = dict()
        params = {
            'q': q, 'count': count,
            'offset': offset,
            'license': 'public',
            'imageType': 'photo',
            # 'imageContent': 'Portrait' # bing is bad ...
        }

        if min_size:
            params['minHeight'] = min_size
            params['minWidth'] = min_size

        if max_size:
            params['maxHeight'] = max_size
            params['maxWidth'] = max_size

        response = requests.get(BingImgAPI.URL,
                                headers=BingImgAPI.HEADER, params=params)
        response.raise_for_status()
        search_results = response.json()
        next_offset = search_results.get('nextOffset')

        img_list = list()
        if search_results.get('value'):
            for d in search_results['value']:
                if d.get('imageId') and d.get('thumbnailUrl'):
                    record = dict()
                    record['id'] = d['imageId']
                    record['url'] = d['thumbnailUrl']
                    img_list.append(record)

        result['next_offset'] = next_offset
        result['img_data'] = img_list

        return result


class ArtistDataBuilder:
    def __init__(self, root_dir: str, artist: str, target=50):
        self.root_dir = root_dir
        self.artist = artist
        self.target = target

        self._pre_setting()

        self.update_count = 0

    def _pre_setting(self):
        FileTool.create_folder(self.root_dir)

        self.artist_dir = f"{self.root_dir}/{self.artist}"
        FileTool.create_folder(self.artist_dir)

        # self.img_dir = f"{self.artist_dir}/img"
        self.img_dir = self.artist_dir
        FileTool.create_folder(self.img_dir)

        self.meta_path = f"{self.artist_dir}/meta.pkl"
        if os.path.exists(self.meta_path):
            self.meta = FileTool.read_pkl(self.meta_path)
        else:
            self.meta = set()

        print(f"meta count: {len(self.meta)}")

    async def _access_image(self, session, img_info):
        result = list()
        img_id = img_info['id']
        url = img_info['url']
        try:
            resp = await session.get(url)
            if resp.status == 200:
                image = np.asarray(bytearray(await resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                result.append(True)
                result.append(img_id)
                result.append(image)
        except Exception as e:
            print(f"failed to convert url to image. url: {url}  Error: {e}")
            result.append(False)
            result.append(img_id)

        return result

    async def _image_downloader(self, data: list) -> list:
        result = list()
        tasks = list()
        async with aiohttp.ClientSession() as session:
            for img_info in data:
                tasks.append(asyncio.create_task(self._access_image(session, img_info)))
            await asyncio.gather(*tasks)
            await session.close()

        for t in tasks:
            if t.result()[0]:
                record = list()
                record.append(t.result()[1])
                record.append(t.result()[2])
                result.append(record)
        return result

    def fetch_images(self, data: list) -> list:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self._image_downloader(data))
        # loop.close()
        return result

    def save_image(self, data):
        result = list()
        image_id = data[0]
        image = data[1]
        count = 0

        capt_faces = FaceCapture.cap(image)
        for i, fb in enumerate(capt_faces, start=1):
            cropped_face = Cropper.get_smart_cropped_face(image, fb)
            if cropped_face is not None:
                rotated = FaceRotate.get_rotated_face(cropped_face)
                if rotated is not None:
                    if RecogTool.can_get_embed(rotated):
                        image_name = f"{FileTool.gen_random_token()}.jpg"
                        img_path = f"{self.img_dir}/{image_name}"
                        cv2.imwrite(img_path, rotated)
                        count += 1

        result.append(image_id)
        result.append(count)
        return result

    def save(self, images):
        with mp.Pool() as pool:
            result = list(
                tqdm(
                    pool.imap(self.save_image, images), total=len(images)
                )
            )

        return result

    def record(self, proc_result: list):
        for r in proc_result:
            img_id = r[0]
            uc = r[1]
            self.meta.add(img_id)
            self.update_count += uc

    def launch(self):
        offset = 0
        flag = True
        while flag:
            print("offset", offset)
            search_result = BingImgAPI.get_img_urls(
                self.artist, offset=offset, count=150
            )

            if search_result['next_offset'] == offset:
                self.clear_empty_dir()
                return

            print(f"query: {len(search_result['img_data'])}")

            if len(search_result['img_data']) == 0:
                self.clear_empty_dir()
                return

            image_queue = list()
            for img_info in search_result['img_data']:
                if not img_info['id'] in self.meta:
                    image_queue.append(img_info)

            if len(image_queue):
                images = self.fetch_images(image_queue)
                proc_result = self.save(images)
                self.record(proc_result)

            if self.update_count >= self.target:
                flag = False

            print('update', self.update_count)

            offset = search_result['next_offset']

        # self.update_meta()
        self.clear_empty_dir()

    def update_meta(self):
        FileTool.to_pkl(self.meta, self.meta_path)

    def clear_empty_dir(self):
        if len(os.listdir(self.img_dir)) == 0:
            os.removedirs(self.img_dir)
            print('cleared empty dir')
