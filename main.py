# coding: utf-8
import os

from service.app.operate import Operate
from service.app.sign_up_helper import SignUpHelper

DEVICE_DATA_PATH = 'DeviceData'
if not os.path.exists(DEVICE_DATA_PATH):
    os.mkdir(DEVICE_DATA_PATH)


def stage_b():
    flag = True
    while flag:
        print('{}, what do you want do?'.format(op.master_data.get('name')))
        print('1 - record master data')
        print('2 - update model')
        print('3 - protect laptop')
        cmd = input()
        if cmd == '1':
            print('ya')
            flag = False

        elif cmd == '2':
            print('coming soon')

        elif cmd == '3':
            print('coming soon')

        else:
            op.hint_unknown_cmd()


def stage_a():
    flag = True
    while flag:
        if op.has_sign_up():
            print('welcome back')
            flag = False
            stage_b()

        else:
            print('hey new face, do you want to sign up? [y/n]')
            cmd = input()
            if cmd in ['y', 'Y']:
                SignUpHelper().launch()
                op.load_master_data()
                flag = False
                stage_b()

            elif cmd in ['n', 'N']:
                op.exit()

            else:
                op.hint_unknown_cmd()


if __name__ == '__main__':
    op = Operate()
    stage_a()
