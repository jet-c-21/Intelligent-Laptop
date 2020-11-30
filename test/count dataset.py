from imutils.paths import list_images

data_path = '../data'

x = list(list_images(data_path))

print(len(x))
