# coding: utf-8
import datetime
import json
import os
import pickle
import random
import shutil
import time
from hashlib import md5


class FileTool:
    @staticmethod
    def save_as_json(data, fp):
        if isinstance(data, set):
            data = list(data)
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_curr_ts():
        return int(str(time.time()).split('.')[0])

    @staticmethod
    def get_date(ts: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(ts)

    @staticmethod
    def create_folder(fp: str):
        if not os.path.exists(fp):
            os.mkdir(fp)

    @staticmethod
    def del_folder(fp: str):
        shutil.rmtree(fp, ignore_errors=True)

    @staticmethod
    def to_pkl(data, fp):
        with open(fp, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def read_pkl(fp):
        with open(fp, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def md5_hash(s: str) -> str:
        m = md5()
        m.update(s.encode("utf-8"))
        h = m.hexdigest()
        return str(h)

    @staticmethod
    def gen_random_token() -> str:
        random_token = ''
        for i in range(4):
            j = random.randrange(0, 3)
            if j == 1:
                a = random.randrange(0, 10)
                random_token += str(a)
            elif j == 2:
                a = chr(random.randrange(65, 91))
                random_token += a
            else:
                a = chr(random.randrange(97, 123))
                random_token += a
        s = f"{FileTool.get_date(FileTool.get_curr_ts())}-{random_token}"
        return FileTool.md5_hash(s)[0:9]
