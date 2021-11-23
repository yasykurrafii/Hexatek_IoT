import socket
import threading
import time
class Server:

    def __init__(self, host = '127.0.0.1', port = 8000, bind = 5):
        self.host = host
        self.port = port
        self.bind = bind
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.connection = []
        self.communication = {}
        self.new_conn = ""

    def up_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.bind)
        print("server up")
        self.thread = threading.Thread(target=self.check_up, args=('192.168.25.2',))
        self.thread.start()
        self.connect()
       
    def connect(self):
         while True:
            try:
                communication, address = self.socket.accept()
                if address[0] not in self.connection:
                    self.connection.append(address[0])
                self.new_conn = address[0]
                print(f'Connected {address[0]}')
                self.communication[address[0]] = communication
            except :
                pass

    
    def receive(self, address):
        communication = self.communication[address]
        message = communication.recv(1024).decode('utf-8')
        if len(message) == 0:
            raise Exception("Message empty")
        return message

    def send(self, address, message):
        communication = self.communication[address]
        communication.send(message.encode('utf-8'))

    def check_up(self, address):
        while True:
            time.sleep(5)
            try:
                self.send(address, "Test Checkup")
                print("Connected")
            except:
                print("Address not connected")



