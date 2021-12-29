import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN)
GPIO.setup(19, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(26, GPIO.IN)
GPIO.setwarnings(False)
GPIO_CH = [6,13,19,26]

while True:
    if GPIO.input(13) == 0 or GPIO.input(19) == 0 or GPIO.input(26) == 0 or GPIO.input(6) == 0:
        lit = [GPIO.input(x) for x in GPIO_CH]
        print(lit)
        print("Halo")
        
    else:
        print("error")
    time.sleep(2)
