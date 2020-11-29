import gdown
import zipfile

dataset_url = 'https://drive.google.com/uc?id=1TCha0-JlGMeuBoMgL0kehK_SsjQ1QKb7'

zip_path = 'data.zip'
print('start downloading dataset ...')
gdown.download(dataset_url, zip_path)
print(f"the dataset zip is download at: {zip_path}")

extract_path = 'data'
print('start extracting dataset ...')
with zipfile.ZipFile(zip_path, 'r') as zf:
    zf.extractall(extract_path)
print(f"the dataset is extracted at: {zip_path}")
