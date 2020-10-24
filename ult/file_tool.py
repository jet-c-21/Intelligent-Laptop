# coding: utf-8
import json

class FileTool:
    @staticmethod
    def save_as_json(data, fp):
        if isinstance(data, set):
            data = list(data)
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


