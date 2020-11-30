# coding: utf-8
import json
import os
import sys


class Operate:
    master_data_path = 'DeviceData/master/master.json'

    def __init__(self):
        self.master_data = dict()

    def load_master_data(self):
        self.master_data = json.load(open(Operate.master_data_path))

    def has_sign_up(self):
        if os.path.exists(Operate.master_data_path):
            self.load_master_data()
            return True
        else:
            return False

    @staticmethod
    def exit():
        sys.exit(0)

    @staticmethod
    def hint_unknown_cmd():
        print('command unknown, please try again! \n')
