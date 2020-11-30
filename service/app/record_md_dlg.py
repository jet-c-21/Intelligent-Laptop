from face_ult.record_master_data import RecordMD
import os
import re

class RecordMasterDataDlg:
    @staticmethod
    def _check_master_data():
        device_dir = 'DeviceData'
        master_dir = f"{device_dir}/master"
        if not os.path.exists(device_dir) or not os.path.exists(master_dir):
            return False

        img_dir = f"{master_dir}/img"
        if len(os.listdir(img_dir)) == 0:
            return False

        return True

    @staticmethod
    def get_input_int():
        p = r'^[1-9][0-9]*$'
        flag = True
        while flag:
            cmd = str(input())
            if re.match(p, cmd):
                return int(cmd)



    @staticmethod
    def launch():
        if RecordMasterDataDlg._check_master_data():
            print('how many data do you want to record? plz type it!')
            fetch_count = RecordMasterDataDlg.get_input_int()
            RecordMD(fetch_count).launch()

        else:
            print('seems you have not have any master data yet, please record 20 master first.')
            RecordMD(20).launch()