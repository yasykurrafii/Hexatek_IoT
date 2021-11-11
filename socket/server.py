import socket
from rasp_con import up_thread, receive

class Server:

    def __init__(self, host = '127.0.0.1', port = 8000, bind = 5):
        self.host = host
        self.port = port
        self.bind = bind
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.connection = []
        self.communication = {}

    def up_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.bind)
        print("server up")
        self.connect()
       
    def connect(self):
         while True:
            try:
                communication, address = self.socket.accept()
                self.connection.append(address[0])
                print(f'Connected {address[0]}')
                up_thread(receive, address[0])
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




