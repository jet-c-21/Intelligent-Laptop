# coding: utf-8
import os

from service.app.operate import Operate
from service.app.record_md_dlg import RecordMasterDataDlg
from service.app.sign_up_helper import SignUpHelper
from service.app.update_model_dlg import UpdateModelDlg
from service.app.protect_laptop_dlg import ProtectLaptopDlg

DEVICE_DATA_PATH = 'DeviceData'
if not os.path.exists(DEVICE_DATA_PATH):
    os.mkdir(DEVICE_DATA_PATH)


def stage_b():
    flag = True
    while flag:
        print('\n{}, what do you want do?'.format(op.master_data.get('name')))
        print('1 - record master data')
        print('2 - update model')
        print('3 - protect laptop')
        print('q - exit\n')
        cmd = input()
        if cmd == '1':
            RecordMasterDataDlg.launch()

        elif cmd == '2':
            UpdateModelDlg.launch()

        elif cmd == '3':
            ProtectLaptopDlg.launch()

        elif cmd == 'q':
            return

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
