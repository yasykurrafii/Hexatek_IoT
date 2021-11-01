import threading
import time
from server import Server

# Connect database
import db

# Global variable for Socket
HOST = '192.168.25.1'
PORT = 9999

server = Server(HOST, PORT)

# Initialize Database
db = db.Database(password='myr170500')

# Checking command
def command(msg):
    com = {'dht' : "(suhu, humidity)",
            'rly' : '(gpio, kondisi)'}
    message = msg.split(" ")
    execute = f"INSERT INTO hexatek.{message[0]} {com[message[0]]} values ({message[1]}, {message[2]})"
    db.execute(execute)

# Function for Socket
def receive(address):
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
        print(f"{address} not connected")

# Function for Thread
def up_thread(func, *args):
    thread = threading.Thread(target=func, args=tuple(args))
    thread.start()
    return thread    

# Main Function
def app():
    up_thread(server.up_server)
    # Connect Server
    
    # address
    address = '192.168.25.2'

    # Up Threading
    up_thread(receive, address)
app()

