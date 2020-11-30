# coding: utf-8
import os
from service.app.operate import Operate
from ult.file_tool import FileTool
import re


class SignUpHelper:
    master_folder = 'DeviceData/master'

    def __init__(self):
        self._master_name = ''
        self._master_email = ''

    def launch(self):
        print('prepare setting master data')
        self.get_master_data()

        # create master folder
        if not os.path.exists(SignUpHelper.master_folder):
            os.mkdir(SignUpHelper.master_folder)
            os.mkdir(f'{SignUpHelper.master_folder}/img')

        # create master json
        data = {'name': self._master_name, 'email': self._master_email}
        save_path = f'{SignUpHelper.master_folder}/master.json'
        FileTool.save_as_json(data, save_path)

        print('finish setting master data')

    def get_master_data(self):
        print('please enter your name:')
        cmd = input()
        self._master_name = cmd

        print('please enter your email:')
        self.ask_mail()

        print('please verify:')
        print(f'Master Name: {self._master_name}')
        print(f'Master Email: {self._master_email}')
        print('correct: y  retype: n')
        flag = True
        while flag:
            cmd = input()
            if cmd in ['y', 'Y']:
                flag = False
            elif cmd in ['n', 'N']:
                self.get_master_data()
            else:
                Operate.hint_unknown_cmd()

    def ask_mail(self):
        p = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        flag = True
        while flag:
            cmd = input()
            if re.match(p, cmd):
                self._master_email = cmd
                flag = False
            else:
                print('please enter a valid mail address! please retry.')
