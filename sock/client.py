import socket
import time
from tkinter import Message

# import sys
# sys.path.append("..")
# from database import db

class Client:

    def __init__(self, host = '127.0.0.1', port = 8000, bind = 5):
        self.host = host
        self.port = port
        self.bind = bind
        self.location = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connection = []
       
    def connecting(self):
        try:
            self.socket.connect(self.location)
            return True
        except:
            return False
    
    def _restart(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connecting()
    
    def receive(self):
        message = self.socket.recv(4096).decode('utf-8')
        return message

    def check_server(self):
        result_conn = self.socket.connect_ex(self.location)
        return result_conn

    def send(self, message):
        print(f"Sending : {message}")
        self._restart()
        self.socket.send(message.encode('utf-8'))

    def get_connection(self):
        self.send('ip')
        while True:
            message = self.receive()
            if message == 'done':
                print("Done")
                break
            ip = message.split(" ")
            self.connection = ip
