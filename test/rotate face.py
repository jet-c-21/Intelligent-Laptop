import cv2

from face_ult.cropper import Cropper
from face_ult.face_capture import FaceCapture
from face_ult.face_rotate import FaceRotate

img_path = 'b.jpg'
image = cv2.imread(img_path)

if __name__ == '__main__':
    capt_faces = FaceCapture.cap(image)
    for i, fb in enumerate(capt_faces, start=1):
        # cropped_face = Cropper.get_cropped_face(image, fb, 0.9)
        cropped_face = Cropper.get_smart_cropped_face(image, fb)
        rotated = FaceRotate.get_rotated_face(cropped_face)
        cf = FaceCapture.cap(rotated)
        print(cf.face_count)

