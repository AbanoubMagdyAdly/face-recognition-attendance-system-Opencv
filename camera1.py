import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class VideoCamera1(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        #success, image = self.video.read()
        # id = 1;

        # sampleN=0;

        # while 1:

        ret, img = self.video.read()

            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # for (x,y,w,h) in faces:

                # sampleN=sampleN+1;

                # cv2.imwrite("facesData/User."+str(id)+ "." +str(sampleN)+ ".jpg", gray[y:y+h, x:x+w])

                # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

                # cv2.waitKey(100)


            # cv2.waitKey(1)

            # if sampleN > 20:

                # break

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
