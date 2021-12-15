import time
import RPi.GPIO as GPIO

from client import Client
import dht_config
from db import Database
from function import up_thread, opening_file

class Main(Client, Database):

    def __init__(self, host='127.0.0.1', port=8000):
        super().__init__(host=host, port=port)
        Database.__init__(self, host, 'rasp1', 'rasp1')
        self.gpio_ch = {'lampu' : [14,15,18,23,24,25,8,7],
                        'saklar' :  [16,20,21]}
        self.setup()
    
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.gpio_ch['lampu'], GPIO.OUT)
        GPIO.setup(self.gpio_ch['saklar'], GPIO.OUT)
        time.sleep(5)
        up_thread(self.inserting_mode, 'lampu', 'rly')
        time.sleep(2)
        up_thread(self.inserting_mode, 'saklar', 'skl')
        time.sleep(2)
        up_thread(self.inserting_dht)
        time.sleep(5)
        up_thread(self.command)

    def command(self):
        while True:
            message = Client.receive(self)
            message = message.split(" ")
            print("Command Active")
            idx = self.gpio_ch.index(int(message[1]))
            if message[0] == 'on':
                GPIO.output(int(message[1]), GPIO.LOW)
                self.mode[idx] = 0
            elif message[0] == 'off':
                GPIO.output(int(message[1]), GPIO.HIGH)
                self.mode[idx] = 1
            elif message == "":
                pass
            Client.send(self, "done")

    def reading_condition(self, gpio : list):
        mode = [GPIO.input(n) for n in gpio]
        return mode

    def inserting_mode(self, checking : str, tabel : str):
        while True:
            modes = self.reading_condition(self.gpio_ch[checking])
            print(modes)
            msg_modes = [str(n) for n in modes]
            message = ','.join(msg_modes)
            
            for ind in range(len(modes)):
                gpio = self.gpio_ch[checking][ind]
                mode = modes[ind]
                command = f'INSERT INTO {tabel}(gpio, kondisi, ip) VALUES ({gpio}, {mode}, "192.168.25.2")'
                super().insert(command)
                message += str(mode) + ','
        
            if checking == 'lampu':
                opening_file("last_condition.txt", 'w', message)
                time.sleep(10)
                continue
            time.sleep(5)
            

    def inserting_dht(self):
        while True:
            dht = dht_config.Suhu()
            if "Error" in dht:
                print("Error dht")
                time.sleep(5)
                continue
            command = f'INSERT INTO dht(suhu, humidity, ip) VALUES ({dht[0]}, {dht[1]}, "192.168.25.2")'
            super().insert(command)
            time.sleep(30)

test = Main(host = "192.168.25.1", port = 9999)