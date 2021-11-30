import time
import RPI.GPIO as GPIO
import dht_config

from server import Server
from db import Database
from function import up_thread

class Main(Server, Database):

    def __init__(self, host='127.0.0.1', port=8000, bind=5):
        super().__init__(host=host, port=port, bind=bind)
        Database.__init__(self, '192.168.25.1', 'rasp1', 'rasp1')
        self.gpio_ch = [14, 15, 18, 23, 24, 25, 8, 7]
        self.setup()
        self.mode = [GPIO.input(n) for n in self.gpio_ch]
        self.host = host

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarning(False)
        GPIO.setup(self.gpio_ch, GPIO.OUT)
        time.sleep(5)
        up_thread(self.inserting_mode)
        up_thread(self.inserting_dht)

    def command(self):
        while True:
            message = super().receive(super().address)
            message = message.split(" ")
            if message[0] == 'on':
                GPIO.output(int(message[1]), GPIO.HIGH)
            elif message[0] == 'off':
                GPIO.output(int(message[1]), GPIO.LOW)
            else:
                super().send(super().address, "Command salah")

    def inserting_mode(self):
        while True:
            self.mode = [GPIO.input(n) for n in self.gpio_ch]
            for ind in range(len(self.mode)):
                gpio = self.gpio_ch[ind]
                mode = self.mode[ind]
                command = f"INSERT INTO rly(gpio, kondisi, ip) VALUES ({gpio}, {mode}, {self.host})"
                super().insert(command)
            time.sleep(30)

    def inserting_dht(self):
        while True:
            dht = dht_config.suhu()
            if "Error" in dht:
                print("Error dht")
                time.sleep(5)
                continue
            command = f"INSERT INTO dht(suhu, humnidity, ip) VALUES ({dht[0]}, {dht[1]}, {self.host})"
            super().insert(command)
            time.sleep(30)

test = Main(host = "192.168.25.3", port= 9999)