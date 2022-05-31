from urllib.request import urlopen
from picamera import PiCamera
from time import sleep
import os

import pyrebase

firebaseConfig = {
    
    'apiKey': "AIzaSyDH3n5SqSt1hGX48joRk1CqyP9OdbW79Xs",
    'authDomain': "warehouse-7b5d5.firebaseapp.com",
    'databaseURL': "https://warehouse-7b5d5-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "warehouse-7b5d5",
    'storageBucket': "warehouse-7b5d5.appspot.com",
    'messagingSenderId': "17994702707",
    'appId': "1:17994702707:web:3d5df1e44366aa34106f06",
    'measurementId': "G-361103K28G"
}

firebase = pyrebase.initialize_app(firebaseConfig)

storage = firebase.storage()

camera = PiCamera()

name = "camera_data.jpg"
camera.capture(name)
print(name+" saved")
storage.child(name).put(name)
print("Image sent")


#baseURL = "192.168.1.6:8080"
#conn=urlopen(baseURL + '/test')