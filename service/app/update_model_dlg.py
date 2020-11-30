import os
from face_ult.model_updater import ModelUpdater


class UpdateModelDlg:
    @staticmethod
    def _check_master_data():
        p = 'DeviceData/master/img'
        data_count = len(os.listdir(p))
        if data_count < 200:
            print(f"your current master data amount is only {data_count} data yet!")
            print(f"for training a model, your master data need to be at least 200.")
            print(f"please recording the master data first!")
            return False

        elif 200 <= len(os.listdir(p)) < 299:
            print(f"your current master data amount is {data_count} yet.")
            print(f"the recommend amount is 300 or greater.")
            print(f"for increasing the accuracy please recording more master data.")
            return True

        else:
            print(f"prepare updating model")
            return True

    @staticmethod
    def launch():
        if UpdateModelDlg._check_master_data():
            ModelUpdater().launch()
