# coding:utf-8
import datetime
import cv2
import smtplib
import imghdr
from ult.file_tool import FileTool
from email.message import EmailMessage


class MailTool:
    ADDRESS = 'jet.bot.service@gmail.com'
    PASSWORD = 'cppai2020'
    DIR = 'temp'

    def __init__(self, master_name, master_email):
        self.master_name = master_name
        self.master_email = master_email

    @staticmethod
    def get_attaches(img_data: list) -> list:
        result = list()
        FileTool.create_folder(MailTool.DIR)
        for img in img_data:
            save_path = f"{MailTool.DIR}/{FileTool.gen_random_token()}.jpg"
            try:
                cv2.imwrite(save_path, img)
                attach_data = MailTool.get_attach_data(save_path)
                result.append(attach_data)
            except Exception as e:
                print(f"failed to save image error: {e}")

        return result

    def send_notification(self, img_data):
        attaches = MailTool.get_attaches(img_data)
        if attaches:
            mail = self.make_mail(self.master_email, attaches)
            MailTool.send(mail)

        FileTool.del_folder(MailTool.DIR)
        print('the notification has sent to master-email')

    def make_mail(self, receiver, attaches):
        subject = f"Hey, {self.master_name}. Here's a laptop security notification!"
        date = datetime.datetime.now()
        content = f"At {date.year}-{date.month}-{date.day}  {date.hour}:{date.minute}:{date.second}, " \
                  f"your laptop might be used by some strangers\n" \
                  f"\n Please check these faces!"

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.master_email
        msg['To'] = receiver
        msg.set_content(content)

        for att in attaches:
            msg.add_attachment(att['data'], filename=att['name'],
                               maintype='image', subtype=att['type'])
        return msg

    @staticmethod
    def get_attach_data(img_path):
        result = dict()
        with open(img_path, 'rb') as f:
            result['data'] = f.read()
            result['type'] = imghdr.what(f.name)
            result['name'] = f.name

        return result

    @staticmethod
    def send(mail):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MailTool.ADDRESS, MailTool.PASSWORD)
            smtp.send_message(mail)
