import os
import re

from face_ult.record_master_data import RecordMD
from ult.ui_tool import UITool
from imutils.paths import list_images


class RecordMasterDataDlg:
    DEVICE_DIR = 'DeviceData'

    @staticmethod
    def _check_master_data() -> bool:
        device_dir = RecordMasterDataDlg.DEVICE_DIR
        master_dir = f"{device_dir}/master"
        if not os.path.exists(device_dir) or not os.path.exists(master_dir):
            return False

        img_dir = f"{master_dir}/img"
        if len(os.listdir(img_dir)) == 0:
            return False

        return True

    @staticmethod
    def _get_master_data_count() -> int:
        return len(list(list_images(RecordMasterDataDlg.DEVICE_DIR)))

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
            curr_count = RecordMasterDataDlg._get_master_data_count()
            print(f"You have {curr_count} of master data now.")
            print('How many data do you want to record this time? plz type it!')
            fetch_count = RecordMasterDataDlg.get_input_int()
            RecordMD(fetch_count).launch()

        else:
            msg = 'Seems that you have not have any master data yet, please record 20 master first.'
            print(msg)
            UITool.msg_window(msg=msg)
            RecordMD(20).launch()
