import RPi.GPIO as GPIO
import time

def LDR(in_pin):
    if GPIO.input(in_pin):
        time.sleep(0.5)
        return False
    else:
        time.sleep(0.5)
        return True


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(3,GPIO.IN)

while True:
    print(f"LDR status: {LDR(3)}")
    time.sleep(2)