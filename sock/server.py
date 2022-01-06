import socket
import threading
import time
import os

from function import up_thread
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
        self.thread = threading.Thread(target=self.check_up)
        self.thread.start()
        self.connect()
       
    def connect(self):
         while True:
            communication, address = self.socket.accept()
            if address[0] not in self.connection:
                self.connection.append(address[0])
            self.new_conn = address[0]
            print(f'Connected {address[0]}')
            self.communication[address[0]] = communication
            up_thread(self.receive, communication)

    
    def receive(self, communication):
        while True:
            message = communication.recv(4096).decode('utf-8')
            print(message)
            if len(message) == 0 or message == 'done':
                break
            elif message == 'ip':
                self.command(communication)
            else:
                message = message.split(" ")
                if message[-1] == '192.168.25.1':
                    print(message)
                else:
                    communication = self.communication[message[-1]]
                    message = " ".join(message[:-1])
                    self.send(communication, message)

    def send(self, communication, message):
        communication.send(message.encode('utf-8'))

    def check_up(self):
        while True:
            if self.connection != []:
                print(self.connection)
                for ip in self.connection:
                    respons = os.system("ping " + ip)
                    if respons:
                        self.connection.remove(ip)
                        del self.communication[ip]
                    time.sleep(5)
                time.sleep(15)
            else:
                print("No one connect")
                time.sleep(10)
                

    def command(self, communication):
        message = " ".join(self.connection)
        self.send(communication, message)
        time.sleep(1.5)
        self.send(communication, 'done')

server = Server(host = '192.168.25.1',port= 9999)
server.up_server()


