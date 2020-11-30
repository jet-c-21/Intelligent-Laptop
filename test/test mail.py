from ult.mail_tool import MailTool
import cv2

img_paths = ['a.jpg', 'b.jpg']
images = []

for p in img_paths:
    images.append(cv2.imread(p))

master_name = 'jet'
master_email = 'edward871130@gmail.com'

m = MailTool(master_name, master_email)

m.send_notification(images)