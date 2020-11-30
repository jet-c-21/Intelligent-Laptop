from imutils import paths

from face_ult.recog_tool import RecogTool

dir_path = '../data'
img_path = list(paths.list_images(dir_path))

if __name__ == '__main__':
    img_path = img_path[0:1]
    print(img_path)
    x = RecogTool.get_face_embed_sequence(img_path)
    print(x)
