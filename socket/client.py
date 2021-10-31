import socket
import time

# import sys
# sys.path.append("..")
# from database import db

class Client:

    def __init__(self, host = '127.0.0.1', port = 8000, bind = 5):
        self.host = host
        self.port = port
        self.bind = bind
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
    def connect(self):
        self.socket.connect((self.host, self.port))
    
    def receive(self, address):
        communication = self.communication[address]
        message = communication.recv(2048).decoder('utf-8')
        message = message.split(' ')
        return message


    def send(self, message):
        self.socket.send(message.encode('utf-8'))
