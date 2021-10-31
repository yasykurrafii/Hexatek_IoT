import tkinter as tk
from tkinter import ttk
import threading
import time
from server import Server

# Connect database
import db

# Global variable for Socket
HOST = '192.168.25.1'
PORT = 9999

server = Server(HOST, PORT)

# Global Variable for GPIO
GPIO_CH = [14,15,18,23,24,25,8, 7]
Button = [0] * 30
mode = [0] * len(GPIO_CH)

# Initialize origin of Tkinter
x_origin = 60
y_origin = 20

x_space = 50
y_space = 30

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

## Function for TKINTER
# def button_sending(address, gpio):
#     time.sleep(0.05)
#     index = GPIO_CH.index(gpio)
#     print(gpio)
#     if mode[index] == 0:
#         send(address, f"on {gpio}")
#         mode[index] = 1
#     elif mode[index] == 1:
#         send(address, f"off {gpio}")
#         mode[index] = 0
#     else:
#         print("Index out of range")
#     configure_button(gpio)

# def change_mode(n, mod):
#     index = GPIO_CH.index(n)
#     mode[index] = mod

# def configure_button(gpio):
#     index = GPIO_CH.index(gpio)
#     if mode[index] == 0:
#         Button[gpio].configure(bg = 'red')
#     elif mode[index] == 1:
#         Button[gpio].configure(bg = 'green')

# def build_button(main_window, address, total = len(GPIO_CH)):
#     x_origin = 60
#     y_origin = 20

#     x_space = 50
#     y_space = 30
#     for i in range(total):
#         gpio = GPIO_CH[i]
#         Button[gpio] = tk.Button(main_window, text = str(gpio), command = lambda x = gpio: up_thread(button_sending, address, x))
#         if i < 4:
#             Button[gpio].place(x = x_origin + x_space * i, y = y_origin + y_space)
#         else:
#             Button[gpio].place(x = x_origin + x_space * (i - 4), y = y_origin + y_space * 3)
#         up_thread(configure_button, gpio)       

# Main Function
def app():
    up_thread(server.up_server)

    # Initialize Tkinter
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Tkinter")

    # Connect Server
    
    # address
    address = '192.168.25.2'

    # Up Threading
    recv = up_thread(receive, address)

    # Desinging TKINTER

    ## Make Tab
    # build_button(root, address)

    root.mainloop()

app()

