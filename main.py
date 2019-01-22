import cv2
import os
import numpy as np
from PIL import Image
from flask import Flask, render_template, Response,request,url_for, session, redirect, request, escape, jsonify
#from _mysql_exceptions import IntegrityError
from camera1 import VideoCamera1
from camera import VideoCamera
#import MySQLdb
import time
import datetime
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
app = Flask(__name__)
app.secret_key = os.urandom(24)
today = datetime.datetime.today();
global error;
error = "";
def seterror(error1):
    global error;
    error=error1;
def setx(x1):
    global x;
    x=x1;
#conn = MySQLdb.connect(host="localhost",user="root",password="",db="atten")
#cursor = conn.cursor()
@app.route('/addone/<string:insert>')
def add(insert):
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO doctor (did, dname,dpass) VALUES (%s, %s,%s)''', (159, insert,258))
	conn.commit()
	return "Done"
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/',methods=['POST','GET'])
def check():	
	try:
		if request.method == 'POST':
			session['id'] = request.form['ID']	
			#return str(session['id'])
		error = None
		id = str(session['id'])
		password = str(request.form["pass"])
		#name = str(request.form["Username"])
		cursor = conn.cursor()
		cursor.execute("SELECT dname FROM doctor WHERE did ='"+id+"' and dpass ='"+password+"'")
		username = str(cursor.fetchall())
		name =str(username).replace("'","").replace("(","").replace(")","").replace(",","")
		cursor.execute("SELECT dtype FROM doctor WHERE did ='"+id+"' and dpass ='"+password+"'")
		user = cursor.fetchall()
		
		if len(user) is 1:
			if user == (('d',),):
				return render_template('index.html',result=name)
			elif user == (('a',),):

				return render_template('index1.html',result=name)
		else:
			error = 'username or password is not valid'
			return render_template('login.html', error=error)
	except TypeError:
		error = 'username or password is not valid'
		return render_template('login.html', error=error)
		
		
@app.route('/index.html/')
def index():
    id = session['id']=1
    if id==session['id']:
        #cursor.execute("SELECT dname FROM doctor WHERE did ='"+id+"'")
        #username = str(cursor.fetchall())
        #name =str(username).replace("'","").replace("(","").replace(")","").replace(",","")
        return render_template('index.html',result="Abanoub")
    else:
        return render_template('login.html')
@app.route('/live.html/')
def live():
	id = session['id']
	if id==session['id']:
		return render_template('live.html')
	else:
		return render_template('login.html')
@app.route('/sections.html/')
def sections():
	sav_sec()
	id = session['id']
	if id==session['id']:
		return render_template('sections.html')
	else:
		return render_template('login.html')	
@app.route('/sections.html/',methods=['GET','POST'])
def sav_sec():
    if request.method == 'POST':
                serv = str(request.form['service'])
                assis = str(request.form["ass"])
                day = str(request.form['day'])
                time =str(request.form['time'])
                lab = str(request.form['lab'])
                msg=None
                error=None
                if request.form['option'] == 'add':
                         try:
                            cursor = conn.cursor()
                            cursor.execute("SELECT did FROM doctor WHERE dname = '"+assis+"'")
                            aid = cursor.fetchone()
                            cursor.execute('''INSERT INTO section(coursecode,labid,time,day,did) VALUES(%s,%s,%s,%s,%s)''',[serv,lab,time,day,aid])
                            conn.commit()
                            msg = 'Section added'
                            return render_template('sections.html',msg=msg)
                         except IntegrityError as IE:
                            error='Lab is busy'
                            return render_template('sections.html',error=error)
                if request.form['option'] == 'delete':
                        cursor = conn.cursor()
                        cursor.execute("SELECT secid FROM section WHERE coursecode = '"+serv+"' AND labid = '"+lab+"' AND time = '"+time+"' AND day = '"+day+"'")
                        secid = str(cursor.fetchone())
                        mystring =str(secid).replace("(","").replace(")","").replace(",","")
                        #return mystring
                        cursor.execute("DELETE FROM section WHERE secid='"+mystring+"'")
                        conn.commit()
                        msg='Section deleted'
                        return render_template('sections.html',msg=msg)
@app.route('/report.html/')
def report():
    id = session['id']
    if id==session['id']:
        cursor.execute("SELECT * FROM section")
        x= cursor.fetchall()
        return render_template('report.html',y=x)
    else:
        return render_template('login.html')
def gen1(camera1):

    while 1:
        frame1 = camera1.get_frame()


        yield (b'--frame1\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen1(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
def gen(camera):

    while 1:
        frame = camera.get_frame()[0];id = camera.get_frame()[1]
        cursor.execute("UPDATE attendance set atten = atten+1 , date = CURDATE() WHERE sid =(SELECT sid FROM student WHERE autoid ='"+id+"') and (secid = '"+x+"' and date != CURDATE())")
        conn.commit();yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed1')
def video_feed1():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/index1.html/')
def index1():
    id = session['id']=1
    if id==session['id']:
        #cursor.execute("SELECT dname FROM doctor WHERE did ='"+id+"'")
        #username = str(cursor.fetchall())
        #name =str(username).replace("'","").replace("(","").replace(")","").replace(",","")
        return render_template('index1.html',result="Abanoub")
    else:
        return render_template('login.html')
@app.route('/live1.html/')
def live1():
	id = session['id']
	if id==session['id']:
		return render_template('live1.html')
	else:
		return render_template('login.html')

@app.route('/att.html/')
def att():
	id = session['id']

	recognizer = cv2.face.LBPHFaceRecognizer_create();

	path="facesData"

	def getImagesWithID(path):

		imagePaths = [os.path.join(path, f) for f in os.listdir(path)]   

     # print image_path   

     #getImagesWithID(path)

		faces = []

		IDs = []

		for imagePath in imagePaths:      

      # Read the image and convert to grayscale

			facesImg = Image.open(imagePath).convert('L')

			faceNP = np.array(facesImg, 'uint8')

            # Get the label of the image

			ID= int(os.path.split(imagePath)[-1].split(".")[1])

             # Detect the face in the image

			faces.append(faceNP)

			IDs.append(ID)

            
		return np.array(IDs), faces

	Ids,faces  = getImagesWithID(path)

	recognizer.train(faces,Ids)

	recognizer.save("trainingdata.yml")
	

	
	if id==session['id']:
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM section")
		result_set = cursor.fetchall()
		return render_template('att.html',x=result_set)


    #return render_template('att.html')
@app.route('/att.html/',methods=['POST','GET'])		
def atten_s():
    id = session['id']
    if id==session['id']:	
        id = request.form["id"]
        course = request.form.get('service')
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE attendance set atten = atten+1 , date = CURDATE() WHERE (sid = '"+id+"') and (secid = '"+course+"' and date != CURDATE())")
        conn.commit()	
        done="Done!"
        seterror(done)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM section")
        result_set = cursor.fetchall()
        return render_template('att.html',x=result_set,done=done)
@app.route('/reg.html/')
def reg():
	id = session['id']
	if id==session['id']:
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM section")
		result_set = cursor.fetchall()
		return render_template('reg.html',x=result_set,result=error)
	else:
		return render_template('login.html')

@app.route('/report1.html/')
def report1():
	id = session['id']
	if id==session['id']:
		return render_template('report1.html')
	else:
		return render_template('login.html')
@app.route('/reg.html/',methods=['POST','GET'])
def detect():
    #try:
       # error = None
        id = session['id']
        if id==session['id']:
            username = str(request.form["name"])
            id = request.form["id"]
            course = str(request.form.get('service'))
            option = request.form["take"]
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance WHERE sid='"+id+"' AND secid='"+course+"'")
            isexist=cursor.fetchone()
            if isexist == None:
                if option == "notakephoto":
                    cursor = conn.cursor()
                    cursor.execute("SELECT sid FROM student WHERE sid='"+id+"'")
                    fetch = cursor.fetchone()
                    if fetch == None:
                        cursor.execute('''INSERT INTO student (sname, sid) VALUES (%s, %s)''', (username, id))
                        cursor.execute('''INSERT INTO attendance (secid, sid,atten,sname) VALUES (%s, %s, %s,%s)''', (course, id, 0,username))
                        conn.commit()
                    else:    
                        if str(id) in fetch:
                            cursor.execute('''INSERT INTO attendance (secid, sid,atten,sname) VALUES (%s, %s, %s,%s)''', (course, id, 0,username))
                            conn.commit()         
  
   

                if option == "takephoto":
                    cursor = conn.cursor()
                    cursor.execute("SELECT sid FROM student WHERE sid='"+id+"'")
                    fetch = cursor.fetchone()
                    if fetch == None:
                        cursor.execute('''INSERT INTO student (sname, sid) VALUES (%s, %s)''', (username, id))
                        cursor.execute('''INSERT INTO attendance (secid, sid,atten,sname) VALUES (%s, %s, %s,%s)''', (course, id, 0,username))
                        conn.commit()
                    else:    
                        if str(id) in fetch:
                            cursor.execute('''INSERT INTO attendance (secid, sid,atten,sname) VALUES (%s, %s, %s,%s)''', (course, id, 0,username))
                            conn.commit()         
                   
   
                    cap = cv2.VideoCapture(0)
                    cursor.execute("SELECT autoid FROM student WHERE sid='"+id+"'")
                    data = cursor.fetchall();
                    for row in data:
                        id=row[0]
                    conn.commit()

                    sampleN=0;

                    while 1:

                        ret, img = cap.read()

                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                        for (x,y,w,h) in faces:

                            sampleN=sampleN+1;

                            cv2.imwrite("facesData/User."+str(id)+ "." +str(sampleN)+ ".jpg", gray[y:y+h, x:x+w])

                            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                            cv2.waitKey(100)

                        cv2.imshow('img',img)

                        cv2.waitKey(1)

                        if sampleN > 30:

                            break

                    cap.release()

                    # cv2.destroyAllWindows()
                    # cursor.execute("SELECT dname FROM doctor WHERE did ='"+id+"'")
                    # username = str(cursor.fetchall())
                    # name =str(username).replace("'","").replace("(","").replace(")","").replace(",","")
                done="Student Registered"
                seterror(done)
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM section")
                result_set = cursor.fetchall()
                return render_template('reg.html',x=result_set,done=done)
            else:  
                notdone="Student already registered"
                seterror(notdone);
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM section")
                result_set = cursor.fetchall()
                return render_template('reg.html',x=result_set,notdone=notdone)                 
        
    # except:
         # error1="Student already Registred"
         # seterror(error1);
         # return reg()
@app.route('/attf.html')
def attf():
	id = session['id']
	if id==session['id']:
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM section")
		result_set = cursor.fetchall();
		return render_template('attf.html',x1=result_set)
	else:
		return render_template('login.html')
@app.route('/attf.html',methods=['POST','GET'])
def attf1():
	id = session['id'];setx(request.form["service"])
	if id==session['id']:
		return render_template('live1.html',x1=request.form["service"])
	else:
		return render_template('login.html')
@app.route('/report.html/',methods=['POST','GET'])
def reports():
    course = request.form["service"]
    cursor = conn.cursor()
    cursor.execute("SELECT * from attendance where secid = (select secid from section where coursecode = '"+course+"')")
    result = cursor.fetchall()
    cursor.execute("SELECT * FROM section")
    y= cursor.fetchall()
    conn.commit()
    return render_template('report.html',x=result,y=y)
@app.route('/report1.html/',methods=['POST','GET'])
def reports1():
    course = request.form["service"]
    cursor = conn.cursor()
    cursor.execute("SELECT * from attendance where secid = (select secid from section where coursecode = '"+course+"')")
    result = cursor.fetchall()
    conn.commit()
    return render_template('report1.html',x=result)
@app.route('/logout')
def dropsession():
    session.pop('id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
