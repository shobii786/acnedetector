from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, current_app, jsonify, make_response
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import MySQLdb
# Define a flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/ad'
db = SQLAlchemy(app)
class Appointment(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    depart = db.Column(db.String(80), nullable=False)
    doctor = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(80), nullable=False)
class User(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
class Contacts(db.Model):   
        sno = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=False)
        email = db.Column(db.String(20), nullable=False)
        phone_num = db.Column(db.String(20), nullable=False)
        msg = db.Column(db.String(120), nullable=False)
        '''
def save_image(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path, 'static/images', photo_name)
    photo.save(file_path)
    return photo_name
'''
@app.route('/signup', methods=['GET','POST'])
def signup():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        entry = User(name=name,email = email,password=password )
        db.session.add(entry)
        db.session.commit()
    return render_template('signup.html')    
    
    name= str(request.form.get('name'))
    password= str(request.form.get('password'))
    email= str(request.form.get('email'))
    cursor=conn.cursor()
    cursor.execute("INSERT INTO user (name,password,email)VALUES(%s,%s,%s)",(name,password,email))
    conn.commit()
    return redirect(url_for('login'))
    

@app.route('/upload2')
def upload2():
    #return render_template('upload2.html')

    if request.method == 'POST':
        
        file=request.files['inputFile']
        newfile= upload(filename=file.filename, image=file.read())
        db.session.add(newfile)
        db.session.commit()
        return 'saved' + file.filename + 'to the database'
    else:
        return render_template('upload2.html')
        
@app.route('/login')

def login():
    
    if(request.method=='POST'):
        email=request.form.get('email')
        password=request.form.get('password')

        usernamedata=db.execute("SELECT email FROM user WHERE email=:email",{'email':email}).fetchone()
        passworddata=db.execute("SELECT password FROM user WHERE email=:email",{'email':email}).fetchone()
        if usernamedata is None:
            return render_template('login.html')
        else:
            for password in passworddata:
                if password == passworddata:
                    return render_template('base.html')
                else:
                    return render_template('login.html')        

    return render_template('login.html')
    

@app.route('/about')

def about():
    return render_template('about.html')
'''
    sno, name phone_num, msg, date, email
       
'''
@app.route('/contact', methods = ['GET', 'POST'])

def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, email = email, phone_num = phone, msg = message )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')
@app.route('/home')

def home():
    return render_template('index.html')

@app.route('/appointment', methods = ['GET', 'POST'])

def appointment():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('date')
        depart = request.form.get('depart')
        doctor = request.form.get('doctor')
        message = request.form.get('message')
        entry = Appointment(name=name, email = email, phone= phone, date= date, depart=depart, doctor=doctor, message=message  )
        db.session.add(entry)
        db.session.commit()
    return render_template('appointment.html')
    
    
    
    if(request.method=='POST'):
        name= request.form.get('name')
        email= request.form.get('email')
        number= request.form.get('number')
        date= request.form.get('date')
        department= request.form.get('department')
        doctor= request.form.get('doctor')
        message= request.form.get('message')
        entry= appointment(Name=name,Email=email,number=number,date=datetime.now(),department=department,doctor=doctor,message=message)
        db.session.add(entry)
        db.session.commit()
        return render_template('appointment.html')        
 
@app.route('/json', methods=['POST'])
def json():
    if request.is_json:
        req= request.get_json()
        response = {

            "message": "JSON_received",
            "name": req.get("name")
        }
        res = make_response(jsonify(response), 200)
        return res
    else:
        res= make_response(jsonify({"message":"No JSON_received"}), 400)    
        return res
@app.route('/doctor')

def doctor():
    return render_template('doctor.html') 

@app.route('/department')

def department():
    return render_template('department.html')           

# Model saved with Keras model.save()
Type_Path = 'model.h5'
MODEL_PATH = 'model.h5'

# Load your trained model
model = load_model(MODEL_PATH)
typeModel = load_model(Type_Path)



def model_predict(img_path, model):
	imag = image.load_img(img_path, target_size=(224,224))

    # Preprocessing the image
	img = image.img_to_array(imag)
    # x = np.true_divide(x, 255)
	img = np.expand_dims(img, axis=0)
	img=img/255

	preds = model.predict(img)
	return preds
@app.route('/payment')
def payment():
    import os
    import sys
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangopaypal_client.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            
        ) from exc
    execute_from_command_line(sys.argv)
    from django.contrib import admin
    from django.urls import path, include
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = 'c5%r461+qett2ao85364cm9omou)xob(+vzj-werh&&o$^e2@l'
    DEBUG = True

    ALLOWED_HOSTS = []

    urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), ]
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
        }
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'base',
        ]

    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]





    return render_template('payment.html')
@app.route('/', methods=['GET'])
def main():
   
 # Main page
    return render_template('login.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    result=''
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        preds = preds.argmax(axis=0)
        if preds[0]==0:
            predictionType = model_predict(file_path,typeModel)
            predictionType=predictionType.argmax(axis=1)
            if predictionType[0]==0:
             result = 'blackheads Medicines: Panadol'
            if predictionType[0]==1:
             result = 'closed_comedo Medicines: Panadol'
            if predictionType[0]==2:
             result = 'cystic Medicines: Panadol'
            if predictionType[0]==3:
             result = 'papules Medicines: Panadol'
            if predictionType==4:
             result = 'pustuler Medicines: Panadol'
            if predictionType[0]==5:
                result = 'Non Acne'
            
        return result
    return None


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')

