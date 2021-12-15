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
        try:
            self.socket.connect(self.binding)
        except:
            raise "Can't Connect to Server"

    def receive(self):
        message = self.socket.recv(4096).decode('utf-8')
        return message

    def send(self, message):
        message = message + " 192.168.25.1"
        self.socket.sendall(message.encode('utf-8'))
