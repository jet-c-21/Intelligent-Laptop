# coding: utf-8
import cv2
import dlib


class Cropper:
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
            img, lt_x, rb_x, lt_y, rb_y = Cropper.pad_img_to_fit_bbox(img, lt_x, rb_x, lt_y, rb_y)
        return img[lt_y:rb_y, lt_x:rb_x, :]

    @staticmethod
    def get_cropped_face(img, face_block: dlib.rectangle, margin='default'):
        if margin == 'default':
            margin = Cropper.MARGIN
        else:
            margin = margin

        lt_x, lt_y, rb_x, rb_y, w, h = face_block.left(), face_block.top(), \
                                       face_block.right() + 1, face_block.bottom() + 1, \
                                       face_block.width(), face_block.height()
        
        lt_ext_x = int(lt_x - margin * w)
        lt_ext_y = int(lt_y - margin * h)
        rb_ext_x = int(rb_x + margin * w)
        rb_ext_y = int(rb_y + margin * h)

        return Cropper.crop_image_to_dimensions(img, lt_ext_x, lt_ext_y, rb_ext_x, rb_ext_y)
