import cv2
import sys
import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from imutils.video.webcamvideostream import WebcamVideoStream
import imutils
import numpy as np
import random
import datetime
import telepot

# email
Pengirim = 'rifaislamet091998@gmail.com'
Password = 'bismillah15091998'
Penerima = 'rifaislamet1509@gmail.com'


def sendEmail(image):
    pesan = MIMEMultipart()
    pesan['Subject'] = 'Penyusup Terdeteksi!'
    pesan['From'] = Pengirim
    pesan['To'] = Penerima

    msgAlternative = MIMEMultipart()
    pesan.attach(msgAlternative)

    msgText = MIMEText('<img src="cid:image1">', 'html')
    msgAlternative.attach(msgText)

    msgImage = MIMEImage(image)
    msgImage.add_header('Content-ID', '<image1>')
    pesan.attach(msgImage)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(Pengirim, Password)
    smtp.sendmail(Pengirim, Penerima, pesan.as_string())
    smtp.quit()


# kamera
class VideoCamera(object):
    def __init__(self, flip=False):
        self.vs = WebcamVideoStream()
        self.flip = flip

    def start(self):
        self.vs.start()

    def close(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_object(self, classifier):
        found_objects = False
        frame = self.flip_if_needed(self.vs.read()).copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(objects) > 0:
            found_objects = True
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes(), found_objects)


# perintah


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print('Got command: %s' % command)
    if command == '/start':
        bot.sendMessage(chat_id, text='''
halo, 
silakan pilih:
1. /pantau
2. /deteksi
''')
    elif command == '/pantau':
        bot.sendMessage(chat_id, text='''sedang memantau..
foto akan segera dikirim...
/kembali''')
    elif command == '/deteksi':
        kamera = VideoCamera()
        kamera.start()
        bot.sendMessage(chat_id, text='''sedang mendeteksi, foto akan dikirim ke email ketika terdapat penyusup
/kembali''')
        email_update_interval = 10
        last_epoch = 0
        klasifikasi_penyusup = cv2.CascadeClassifier("facial_recognition_model.xml")

        def check_for_objects():
            global last_epoch
            while True:
                try:
                    frame, found_obj = kamera.get_object(klasifikasi_penyusup)
                    if found_obj and (time.time() - last_epoch) > email_update_interval:
                        last_epoch = time.time()
                        print("Sedang mengirim foto...")
                        sendEmail(frame)
                        print("selesai!")
                except:
                    print("Ada kesalahan pengiriman!")

        if __name__ == '__main__':
            t = threading.Thread(target=check_for_objects, args=())
            t.start()

    elif command == '/kembali':
        # kasih perintah close
        kamera.close()
        bot.sendMessage(chat_id, text='''halo,
silakan pilih:
1. /pantau
2. /deteksi
''')


bot = telepot.Bot('token')
bot.message_loop(handle)
while 1:
    time.sleep(10)
