import socket
from function import up_thread


class Server:

    def __init__(self, host = '127.0.0.1', port = 8000, bind = 5):
        self.host = host
        self.port = port
        self.bind = bind
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.communication = {}
        self.address = ""
        self.up_server()

    def up_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.bind)
        print("Server Up")
        up_thread(self.connect)

    def connect(self):
        while True:
            try:
                communication, address = self.socket.accept()
                print(f"Connect {address[0]}")
                self.communication[address[0]] = communication
                self.address = address[0]
            except:
                pass

    def receive(self, address):
        communication = self.communication[address]
        message = communication.recv(2048).decode('utf-8')
        return message
    
    def send(self, address, message):
        communication = self.communication[address]
        communication.send(message.encode('utf-8'))
