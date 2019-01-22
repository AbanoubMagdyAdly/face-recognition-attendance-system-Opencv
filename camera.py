import cv2
import numpy as np
import os
from PIL import Image
from flask import Flask, render_template, Response,request,url_for, session, redirect, request, escape, jsonify
import MySQLdb
import time
import datetime
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("trainingdata.yml")
conn = MySQLdb.connect(host="localhost",user="root",password="",db="atten")
global x1;
class VideoCamera(object):
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

        ret, img = self.video.read();
        id=0;
        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (255, 255, 255)
        while 1:	
            ret, img = self.video.read()
            locy = int(img.shape[0]/2) # the text location will be in the middle
            locx = int(img.shape[1]/2) #of the frame for this example
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.5, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                id,conf=rec.predict(gray[y:y+h,x:x+w])
                id1=str(id);
                cv2.putText(img, id1, (x, y), fontFace, fontScale, fontColor) 
                ret, jpeg = cv2.imencode('.jpg', img)
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
                d=time.strftime("%Y-%m-%d")
                cursor.execute(	"SELECT atten FROM attendance WHERE sid =%s and secid=%s", ("SELECT sid FROM student WHERE autoid ='"+str(id)+"", "x1"))
                atten=cursor.fetchall()
                cursor.execute("update attendance set atten = atten+1 , date = CURDATE() where sid =%s and secid =%s and date != %s", ("SELECT sid FROM student WHERE autoid ='"+str(id)+"", "x1" ,d))
                conn.commit()
                return [jpeg.tobytes(),id1]

     #       return  render_template('index1.html')	