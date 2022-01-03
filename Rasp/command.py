import time
import RPi.GPIO as GPIO

from client import Client
import dht_config
from function import up_thread
import threading

class Command(Client):

    def __init__(self, host='127.0.0.1', port=8000):
        super().__init__(host=host, port=port)
        self.gpio_ch = {'lampu' : [14,15,18,23,24,25,8,7],
                        'saklar' :  [6,13,19,26]}
        self.mode = []
        self.stop_thread = False
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.gpio_ch['lampu'], GPIO.OUT)
        GPIO.setup(self.gpio_ch['saklar'], GPIO.IN)
        self.mode = [GPIO.input(x) for x in self.gpio_ch['lampu']]
        self.command()

    def command(self):
        while True:
            print("Command")
            message = super().receive()
            print(message)
            message = message.split(" ")
            print("Command Active")
            idx = self.gpio_ch['lampu'].index(int(message[1]))
            if message[0] == 'on':
                GPIO.output(int(message[1]), GPIO.LOW)
                self.mode[idx] = 0
            elif message[0] == 'off':
                GPIO.output(int(message[1]), GPIO.HIGH)
                self.mode[idx] = 1
            elif message == "":
                pass
            print("done")

test = Command(host = "192.168.25.1", port = 9999)