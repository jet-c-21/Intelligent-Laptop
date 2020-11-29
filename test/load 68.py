import dlib
import os
import pathlib
from face_ult.model_api import ModelAPI
import ntpath


# # path = '../face_ult/model/official/dlib/shape_predictor_68_face_landmarks.dat'
#
# path = '..\\face_ult\\model\\official\\dlib\\shape_predictor_68_face_landmarks.dat'
#
# path = pathlib.Path(path)
# #
# # os.path.abspath(path)
# #
# # print(path)

# p = ModelAPI.get_path('dlib-lmk68')
#
# x = ntpath.abspath(p)
# print(x)
# print(p)
#
# p = 'D:/CODING/TARGET-PROJECT/Intel-lapt-desktop/Intelligent-Laptop/face_ult/model/official/dlib/shape_predictor_68_face_landmarks.dat'
# x = dlib.shape_predictor(p)

# p = ModelAPI.get_path('dlib-lmk68', 'unix')
# x = dlib.shape_predictor(p)
# print(p)
# print(type(p))

p = ModelAPI.get('dlib-lmk68')
print(p)
