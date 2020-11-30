# coding: utf-8
import cv2
import dlib
import numpy as np

from face_ult.face_capture import FaceCapture


class BboxCropper:
    MARGIN = 0.5

    @staticmethod
    def pad_img_to_fit_bbox(img, lt_x, rb_x, lt_y, rb_y):
        img = cv2.copyMakeBorder(img, - min(0, lt_y), max(rb_y - img.shape[0], 0),
                                 -min(0, lt_x), max(rb_x - img.shape[1], 0), cv2.BORDER_REPLICATE)
        rb_y += -min(0, lt_y)
        lt_y += -min(0, lt_y)
        rb_x += -min(0, lt_x)
        lt_x += -min(0, lt_x)
        return img, lt_x, rb_x, lt_y, rb_y

    @staticmethod
    def crop_image_to_dimensions(img, lt_x, lt_y, rb_x, rb_y):
        if lt_x < 0 or lt_y < 0 or rb_x > img.shape[1] or rb_y > img.shape[0]:
            img, lt_x, rb_x, lt_y, rb_y = BboxCropper.pad_img_to_fit_bbox(img, lt_x, rb_x, lt_y, rb_y)
        return img[lt_y:rb_y, lt_x:rb_x, :]

    @staticmethod
    def get_cropped_face(img, face_block: dlib.rectangle, margin='default'):
        if margin == 'default':
            margin = BboxCropper.MARGIN
        else:
            margin = margin

        lt_x, lt_y, rb_x, rb_y, w, h = face_block.left(), face_block.top(), \
                                       face_block.right() + 1, face_block.bottom() + 1, \
                                       face_block.width(), face_block.height()

        lt_ext_x = int(lt_x - margin * w)
        lt_ext_y = int(lt_y - margin * h)
        rb_ext_x = int(rb_x + margin * w)
        rb_ext_y = int(rb_y + margin * h)

        return BboxCropper.crop_image_to_dimensions(img, lt_ext_x, lt_ext_y, rb_ext_x, rb_ext_y)


class Cropper:
    MARGIN = 0.5

    @staticmethod
    def get_proper_margin(w: int, h: int, lt_x: int, lt_y: int, margin: float) -> float:
        w_expand = int(w * margin)
        h_expand = int(h * margin)

        new_lt_x = lt_x - w_expand
        new_lt_y = lt_y - h_expand

        if new_lt_x > 0 and new_lt_y > 0:
            delta_w = abs(new_lt_x - lt_x)
            delta_h = abs(new_lt_y - lt_y)
            proper_margin = max(delta_w / w, delta_h / h)

        else:
            if new_lt_x < 0:
                new_lt_x = 0

            if new_lt_y < 0:
                new_lt_y = 0

            delta_w = abs(new_lt_x - lt_x)
            delta_h = abs(new_lt_y - lt_y)
            proper_margin = min(delta_w / w, delta_h / h)

        return int(proper_margin * 100) / 100

    @staticmethod
    def get_cropped_face(img: np.ndarray, face_block: dlib.rectangle, margin=None) -> np.ndarray:
        if margin:
            margin = margin
        else:
            margin = BboxCropper.MARGIN

        w = face_block.width()
        h = face_block.height()
        lt_x = face_block.left()
        lt_y = face_block.top()

        margin = Cropper.get_proper_margin(w, h, lt_x, lt_y, margin)

        w_expand = int(w * margin)
        h_expand = int(h * margin)
        new_lt_x = lt_x - w_expand
        new_lt_y = lt_y - h_expand
        new_w = w + (2 * w_expand)
        new_h = h + (2 * h_expand)

        return img[new_lt_y:new_lt_y + new_h, new_lt_x:new_lt_x + new_w]

    @staticmethod
    def get_smart_cropped_face(img: np.ndarray, face_block: dlib.rectangle):
        for i in range(10, -1, -1):
            margin = i / 10
            cropped = Cropper.get_cropped_face(img, face_block, margin)
            h, w, _ = cropped.shape
            if h > 0 and w > 0:
                capt_faces = FaceCapture.cap(cropped)
                if capt_faces.face_count == 1:
                    return cropped
