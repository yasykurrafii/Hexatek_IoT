import threading
import time
from server import Server

# Connect database
import db
db = db.Database(password='myr170500')

# Global variable for Socket
HOST = '192.168.25.1'
PORT = 8888

server = Server(HOST, PORT)

# Checking command
def command(msg):
    com = {'dht' : "(suhu, humidity, ip)",
            'rly' : '(gpio, kondisi, ip)'}
    daerah = {'jakarta': '192.168.25.2',
            'bekasi' : '192.168.25.3'}
    message = msg.split(" ")
    ip = daerah[message[3]]
    execute = f"INSERT INTO hexatek.{message[0]} {com[message[0]]} values ({message[1]}, {message[2]}, '{ip}')"
    db.insert(execute)

# Function for Socket
def receiving(address):
    while True:
        try:
            message = server.receive(address)
            print(message)
            up_thread(command, message)
        except :
            print(f'{address} not connected')
            time.sleep(5.0)
            pass

def send(address, message):
    try:
        time.sleep(0.5)
        server.send(address, message)
    except KeyError:
        print(f"{message}")
        print(f"{address} not connected")
        if address == "192.168.25.1":
            app()

# Function for Thread
def up_thread(func, *args):
    thread = threading.Thread(target=func, args=tuple(args))
    thread.start()
    return thread    

# Function to get connection
def get_connection():
    return server.connection

def up_receive():
    new_conn = ""
    current = ""
    while True:
        if new_conn != current:
            current = new_conn
            up_thread(receiving, current)
        else:
            new_conn = server.new_conn
        time.sleep(2)

# Main Function
def app():
    up_thread(server.up_server)
    up_thread(up_receive)