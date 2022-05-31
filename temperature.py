import RPi.GPIO as GPIO
import time
import adafruit_dht
from board import*

def dht():
    for i in range(5):
        m.measure()
        h = m.humidity
        t = m.temperature
        time.sleep(2)
        return (t,h)


sensorpin = D4
m = adafruit_dht.DHT11(sensorpin, use_pulseio=False)
while True:
    time.sleep(2)
    (temp, humidity) = dht()
    print(temp)
    print(humidity)