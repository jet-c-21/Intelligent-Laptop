import pathlib
import random

import numpy as np
from imutils import paths
from joblib import dump
from scipy.sparse import coo_matrix
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.utils import shuffle
from tqdm import tqdm

from face_ult.recog_tool import RecogTool


class ModelUpdater:
    DEVICE_DATA_DIR = f"{pathlib.Path(__file__).parent.parent}/DeviceData"
    DATASET_DIR = f"{pathlib.Path(__file__).parent.parent}/data"
    SAVE_DIR = f"{pathlib.Path(__file__).parent}/model/custom"

    def __init__(self):
        self.X = list()
        self.y = list()
        self.test_size = 0.2
        self.cv = 10
        self.master_count = 0
        self.stranger_count = 0
        self.score = None
        self.model = None
        self.model_name = None
        self.model_path = None

    def load_master_data(self):
        img_paths = list(paths.list_images(ModelUpdater.DEVICE_DATA_DIR))
        for p in tqdm(img_paths):
            embed = RecogTool.get_face_embed(p)
            if embed is not None:
                self.X.append(embed)
                self.y.append(1)
                self.master_count += 1

    def load_stranger_data(self):
        img_paths = list(paths.list_images(ModelUpdater.DATASET_DIR))
        random.shuffle(img_paths)
        for p in tqdm(img_paths):
            embed = RecogTool.get_face_embed(p)
            if embed is not None:
                self.X.append(embed)
                self.y.append(0)
                self.stranger_count += 1

            if self.stranger_count == self.master_count:
                break

    def train(self):
        svc_clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
        self.score = np.mean(cross_val_score(svc_clf, self.X, self.y, cv=self.cv))
        X_sparse = coo_matrix(self.X)
        X, X_sparse, y = shuffle(self.X, X_sparse, self.y, random_state=777)
        svc_clf.fit(X, y)
        self.model = svc_clf

    def save_model(self):
        self.model_name = str(int(self.score * (10 ** 6)))
        self.model_path = f"{ModelUpdater.SAVE_DIR}/{self.model_name}.joblib"
        dump(self.model, self.model_path)

    def launch(self):
        self.load_master_data()
        print(f"[INFO] - finish loading master data and convert to training data, count: {self.master_count}")

        self.load_stranger_data()
        print(f"[INFO] - finish loading stranger data and convert to training data, count: {self.master_count}")

        self.train()
        print(f"[INFO] - Model Score: {self.score} CV: {self.cv}")

        self.save_model()
        print(f"[INFO] - Model Saved - {self.model_path}")
