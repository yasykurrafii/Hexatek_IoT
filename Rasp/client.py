import socket
import time

from function import *

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.binding = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__setup()

    def __setup(self):
        self.__connect()

    def __connect(self):
        self.socket.connect(self.binding)

    def receive(self):
        self.send("Halo")
        message = self.socket.recv(4096).decode('utf-8')
        print(message)
        return message

    def send(self, message):
        message = message + " 192.168.25.1"
        self.socket.sendall(message.encode('utf-8'))
