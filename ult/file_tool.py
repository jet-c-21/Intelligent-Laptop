# coding: utf-8
import json
import time
import datetime


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
