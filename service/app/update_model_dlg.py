import os
from ult.ui_tool import UITool
from face_ult.model_updater import ModelUpdater


class UpdateModelDlg:
    @staticmethod
    def _check_master_data():
        p = 'DeviceData/master/img'
        data_count = len(os.listdir(p))
        if data_count < 200:
            msg = f"Your current master data amount is only {data_count} yet! \n" \
                  f"For training a model, your master data need to be at least 200. \n" \
                  f"Please recording the master data first!"
            print(msg)
            UITool.msg_window(msg=msg)
            return False

        elif 200 <= len(os.listdir(p)) < 299:
            msg = f"Your current master data amount is {data_count} yet. \n" \
                  f"The recommend amount is 300 or greater. \n" \
                  f"For increasing the accuracy, please recording more master data."
            print(msg)
            UITool.msg_window(msg=msg)
            return True

        else:
            print(f"prepare updating model")
            return True

    @staticmethod
    def launch():
        if UpdateModelDlg._check_master_data():
            ModelUpdater().launch()
