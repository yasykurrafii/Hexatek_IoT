import time
import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter import font
from PIL import Image, ImageTk

from db import Database
from function import *

from client import Client

clien = Client('192.168.25.1', 9999)
up_thread(clien.connecting)
time.sleep(3)

get_connection = up_thread(clien.get_connection)
get_connection.join()


db = Database(password = 'myr170500')

# class Connecting(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Connecting")
#         self.__create_widget()

#     def __create_widget(self):
#         ttk.Label(self, text="Connecting to Server....").pack()

class ImageLampu(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.img1 = (Image.open('img\lampu.png')).resize((50, 50), Image.ANTIALIAS)
        self.img2 = (Image.open('img\lampuon.png')).resize((50,50), Image.ANTIALIAS)
        self.on = ImageTk.PhotoImage(self.img2)
        self.off = ImageTk.PhotoImage(self.img1)

        self.__create_widget()
    
    def __create_widget(self):
        ttk.Label(self, image= self.on).grid(row=3, column=0, pady=10, padx=2)
        ttk.Label(self, image= self.off).grid(row=3, column=1, pady=10, padx=2)
        ttk.Label(self, image= self.on).grid(row=3, column=2, pady=10, padx=2)
        ttk.Label(self, image= self.off).grid(row=3, column=3, pady=10, padx=2)

class LabelSuhu(ttk.Frame):
    global db
    def __init__(self,container, ip):
        super().__init__(container)
        self.data = db.take_data(table = 'dht', data = 'all', ip = ip)
        self.ip = ip
        self.data_new = self.data[-1]
        self.fnt = ('Helvetica', 20, 'bold')
        self.label = ttk.Label(self, text = '.')
        self.humidity = ttk.Label(self, text = '.')
        self.label.grid(row=1, column=0, columnspan=2, pady=0, padx=30)
        self.humidity.grid(row=1, column=2, columnspan=2, pady=0, padx=30)
        self.__create_widget()
        up_thread(self.__config)

    def __create_widget(self):
        suhu = int(self.data_new[1])
        font_title = ('Helvetica', 20)
        ttk.Label(self, text= "Temp", font=font_title).grid(row = 0, column= 0, columnspan=2, pady=0, padx=30)
        text = str(self.data_new[1])
        self.__change_color(suhu, text)
        ttk.Label(self, text = "Humid", font=font_title). grid(row=0, columnspan=2, column=2, pady=0, padx=30)
        self.humidity.configure(text = self.data_new[2], font=self.fnt)
    
    def __config(self):
        while True:
            data_suhu = db.take_data(table = 'dht', data = 'all', ip = self.ip)
            data_new = data_suhu[-1]
            text_humid = str(data_new[2])
            suhu = data_new[1]
            text = str(data_new[1])
            self.__change_color(suhu, text)
            self.humidity.configure(text=text_humid)
            time.sleep(5)

    def __change_color(self, suhu, text):
        if suhu < 30:
            self.label.configure(text= text, foreground='green', font=self.fnt)
        elif suhu >=30 and suhu <=35:
            self.label.configure(text= text, foreground='orange', font=self.fnt)
        elif suhu > 35:
            self.label.configure(text= text, foreground='red', font=self.fnt)

class ButtonToggle(ttk.Frame):
    global clien

    def __init__(self, container, grid, text, background, ip):
        super().__init__(container)
        self.text = text
        self.ip = ip

        # If Else nentuin command
        if background == 'green':
            self.button = tk.Button(container, text = text, command=self.__command_off, bg=background, height='2', width='10')
        elif background=='red':
            self.button = tk.Button(container, text = text, command=self.__command_on, bg=background, height='2', width='10')
        self.button.grid(row=grid[0], column=grid[1])

    ## Command untuk on or off
    def __command_on(self):
        clien.send(f'on {self.text} {self.ip}')
        self.button.configure(bg='green', command=self.__command_off)
    
    def __command_off(self):
        clien.send(f'off {self.text} {self.ip}')
        self.button.configure(bg='red', command=self.__command_on)

class ButtonWidget(ttk.Frame):
    global db

    def __init__(self, container, ip):
        super().__init__(container, padding=20)
        self.ip = ip
        self.data = db.take_data(table = 'rly', data = 'all', ip=ip)
        self.button_collection = []
        self.__create_widget()

    def __create_widget(self):
        data = db.take_data('rly', ip= self.ip)[-8:]
        gpio = [14, 15, 18, 23, 24, 25, 8, 7]

        column_row = [
            [1,0],
            [1,1],
            [1,2],
            [1,3],
            [2,0],
            [2,1],
            [2,2],
            [2,3],
        ]
        for i in range(len(gpio)):
            condition = data[i][2]
            if condition == 0:
                ButtonToggle(self, column_row[i], gpio[i], 'green', self.ip)
            else:
                ButtonToggle(self, column_row[i], gpio[i], 'red', self.ip)

class Tampilan(tk.Frame):

    def __init__(self, container, connected,text, ip):
        super().__init__(container, highlightbackground = 'black', width = '300', height = '300', pady = 30)
        self.ip = ip
        self.text = text
        if connected:
            self.__create_widget()
        else:
            self.__not_connected()


    def __create_widget(self):
        tk.Label(self, text=self.text).grid(row=0, column=0)
        bt1 = ButtonWidget(self, self.ip)
        image = ImageLampu(self)
        suhu = LabelSuhu(self, self.ip)
        bt1.grid(row=1, column=0)
        image.grid(row=2, column=0)
        suhu.grid(row=3, column=0)
 
    def __not_connected(self):
        ttk.Label(self, text=f"{self.ip} not connected").grid(row=0, column=0, padx=10)

class App(tk.Tk):
    global clien
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.title("Monitoring Raspberry")
        self.resizable(False, False)

        self.ip, self.name = self.__listing_ip("ip.txt")

        self.__create_widget()

    def __create_widget(self):
        row_column = [
            [0,0],
            [0,1],
            [0,3],
            [1,0],
            [1,1]
        ]
        connection = clien.connection
        for index in range(len(row_column)):
            if self.ip[index] in connection:
                tampilan = Tampilan(self, True, self.name[index], self.ip[index])
            else:
                tampilan = Tampilan(self, False, self.name[index], self.ip[index])
            tampilan.grid(row=row_column[index][0], column=row_column[index][1], pady=30)

        tk.Button(self, text="EXIT", height=2, width=15,command=lambda:[clien.send("done") ,self.destroy()], bg='red', pady=10).grid(row=2, column=3, columnspan=2)

    def __listing_ip(self, file):
        with open(file, "r") as f:
            list_ip = []
            frame_text = []
            for x in f:
                if x[-1] == "\n":
                    x = x[:-1]
                line = x.split(" ")
                ip = line[-1]
                name = line[0]
                list_ip.append(ip)
                frame_text.append(name)
            return list_ip, frame_text

app = App()
app.mainloop()
