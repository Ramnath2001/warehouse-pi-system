import RPi.GPIO as GPIO
import time

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

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(27,GPIO.IN)

while True:
    print('Distance1: %0.2f m' % ultra(17,27))
    time.sleep(2)