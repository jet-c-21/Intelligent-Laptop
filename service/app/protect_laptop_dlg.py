from service.app.operate import Operate
from face_ult.fd_protect import FDProtect
from face_ult.fm_protect import FMProtect
from face_ult.model_api import ModelAPI
import os

class ProtectLaptopDlg:
    @staticmethod
    def _check_master_data():
        p = 'DeviceData/master/img'
        data_count = len(os.listdir(p))
        if data_count >= 20:
            return True
        else:
            need = 20 - data_count
            print(f"your master data is lower than 20, plz record {need} more.")
            return False

    @staticmethod
    def launch():
        flag = True
        while flag:
            print(f"which mode do you want to use?")
            print(f'1 - face distance')
            print(f'2 - face model')
            print(f'3 - demo mode')
            print(f'b - back')
            cmd = input()
            if cmd == '1':
                ProtectLaptopDlg.face_distance_handler()
                return

            elif cmd == '2':
                ProtectLaptopDlg.face_model_handler()
                return

            elif cmd == '3':
                ProtectLaptopDlg.demo_handler()
                return

            elif cmd == 'b':
                return

            else:
                Operate.hint_unknown_cmd()

    @staticmethod
    def face_distance_handler():
        if ProtectLaptopDlg._check_master_data():
            FDProtect().launch()

    @staticmethod
    def face_model_handler():
        if ModelAPI.get_path('custom'):
            FMProtect().launch()
        else:
            print('you have not had any custom model yet. plz try to update the model first.')

    @staticmethod
    def demo_handler():
        FMProtect('demo').launch()

