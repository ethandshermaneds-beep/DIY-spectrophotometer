import RPi.GPIO as GPIO
import time

LED = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
time.sleep(15)
GPIO.output(LED, GPIO.HIGH)
