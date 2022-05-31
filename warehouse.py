#! /usr/bin/python3
import RPi.GPIO as GPIO
import time
import adafruit_dht
from picamera import PiCamera
import os
import pyrebase
from urllib.request import urlopen
from board import*

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

def LDR(in_pin):
    if GPIO.input(in_pin):
        time.sleep(0.5)
        return False
    else:
        time.sleep(0.5)
        return True

def dht():
    try:
        m.measure()
        h = m.humidity
        t = m.temperature
        time.sleep(2)
        return (t,h)
    except:
        return (0,0)

def ultra(trig, echo):
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(trig, GPIO.LOW)
    while not GPIO.input(echo):
        pass
    t1 = time.time()
    while GPIO.input(echo):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

def cam_module():
    try:
        name = "camera_data.jpg"
        camera.capture(name)
        print(name+" saved")
        storage.child(name).put(name)
        print("Image sent")
        sleep(2)
    except:
        camera.close()
        
def send_server_request():
    baseURL = "http://192.168.43.95:8080"
    conn=urlopen(baseURL + '/test')
    s = str(conn.read())
    l = s.split('"')
    l = l[1].split("[")
    l = l[1].split("]")
    l = l[0].split("'")
    result = l[1]
    result_index = l[3]
    print(result)
    print(result_index)
    conn.close()
    return result
    
def remove_data(filename):
    os.remove(filename)
    
def rename_data(filename, newFilename):
    os.rename(filename, newFilename)
    


#Ultra sonic pin assignment
GPIO.setup(17,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(27,GPIO.IN)
#GPIO.setup(11,GPIO.OUT,initial=GPIO.LOW)
#GPIO.setup(13,GPIO.IN)

#LDR pin assignment
GPIO.setup(3,GPIO.IN)
channel_api = "https://api.thingspeak.com/update?api_key=HTZD89I9CYCGF6Y2"
#LED setup
pins = [10,9,25]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output
    GPIO.output(pin, GPIO.HIGH)

#DHT11 pin assignment adafruit
sensorpin = D4
m = adafruit_dht.DHT22(sensorpin, use_pulseio=False)
time.sleep(2)
try:
    while True:
        dist = round(ultra(17,27),2)
        ldr = LDR(3)
        ldr_status = 0
        if ldr:
            ldr_status = 1
        (temp, humidity) = dht()
        print('Distance: %0.2f m' % dist)
        print(f"LDR status: {ldr_status}")
        print(f"Temp and Humidity Value: {(temp, humidity)}")
        
        if(dist < 0.18 or ldr_status == 1):
            GPIO.output(9, GPIO.LOW)
            cam_module()
            GPIO.output(10, GPIO.LOW)
            result = send_server_request()
            if result == "Rats":
                GPIO.output(25, GPIO.LOW)
                GPIO.output(10, GPIO.HIGH)
                conn=urlopen(channel_api + f'&field1={dist}&field2={temp}&field3={humidity}&field4={ldr_status}&field5=0&field6=0&field7=1')
                print(conn.read())
                conn.close()
            elif result == "Human":
                GPIO.output(25, GPIO.LOW)
                GPIO.output(10, GPIO.HIGH)
                conn=urlopen(channel_api + f'&field1={dist}&field2={temp}&field3={humidity}&field4={ldr_status}&field5=0&field6=1&field7=0')
                conn.close()
            elif result == "Fire":
                GPIO.output(25, GPIO.LOW)
                GPIO.output(10, GPIO.HIGH)
                conn=urlopen(channel_api + f'&field1={dist}&field2={temp}&field3={humidity}&field4={ldr_status}&field5=1&field6=0&field7=0')
                conn.close()
            else:
                GPIO.output(10, GPIO.HIGH)
                GPIO.output(9, GPIO.HIGH)
                print("Nothing to worry about")
        elif humidity > 70:
            conn=urlopen(channel_api + f'&field1={dist}&field2={temp}&field3={humidity}&field4={ldr_status}&field5=0&field6=0&field7=0&field8=1')
            print(conn.read())
            conn.close()
        else:
            conn=urlopen(channel_api + f'&field1={dist}&field2={temp}&field3={humidity}&field4={ldr_status}&field5=0&field6=0&field7=0')
            print(conn.read())
            conn.close()
        
        time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()




