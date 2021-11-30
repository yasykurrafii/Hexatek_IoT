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
        self.location = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
    def connecting(self):
        try:
            self.socket.connect(self.location)
            return True
        except:
            return False
    
    def receive(self, address):
        communication = self.communication[address]
        message = communication.recv(2048).decoder('utf-8')
        message = message.split(' ')
        return message

    def check_server(self):
        result_conn = self.socket.connect_ex(self.location)
        print(f"{self.host} result {result_conn}")
        return result_conn
    
    def close_conn(self):
        self.socket.close()

    def send(self, message):
        self.socket.send(message.encode('utf-8'))