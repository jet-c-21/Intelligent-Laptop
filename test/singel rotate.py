from face_ult.face_rotate import FaceRotate
from face_ult.face_capture import FaceCapture
from face_ult.cropper import Cropper
import cv2

from face_ult.display_tool import DisplayTool as dt

img_path = 'bts.jpg'
image = cv2.imread(img_path)
print(image.shape)

if __name__ == '__main__':
    capt_faces = FaceCapture.cap(image)
    face_block = capt_faces[0]
    cropped_face = Cropper.get_cropped_face(image, face_block, 0.9)

    print(cropped_face.shape)

    # print(cropped_face.shape)

    # dt.view(cropped_face)
