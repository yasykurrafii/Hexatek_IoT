import time
import tkinter as tk
from tkinter import Button, Toplevel, ttk
from tkinter import font
from tkinter.constants import FALSE, TRUE
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

from db import Database
from function import up_thread, up_thread_daemon

from client import Client

clien = Client('192.168.25.1', 9999)
up_thread(clien.connecting)
time.sleep(3)

get_connection = up_thread(clien.get_connection)
get_connection.join()


db = Database(password = 'myr170500')

f = Figure(figsize = (5,5), dpi = 100)
a = f.add_subplot(111)

IP = []

def button_name():
    button = {}
    with open('button.txt', 'r') as f:
        new = True
        ip = ""
        for x in f:
            x = x.split(':')
            if new:
                key = x[0][:-1]
                button[key] = []
                ip = key
                new = False
            else:
                if x[-1][-1] == '\n':
                    name = x[-1][:-1]
                else:
                    name = x[-1]
                button[ip].append(name)
            if len(x) == 1 and x[0] == '\n':
                new = True
    for x in button.keys():
        button[x] = button[x][:6]
    return button
Button_Name = button_name()

# class Connecting(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Connecting")
#         self.__create_widget()

#     def __create_widget(self):
#         ttk.Label(self, text="Connecting to Server....").pack()

STOP_THREAD = FALSE

DATA = {'192.168.25.2' : {'skl': [], 'suhu' : ()},
        '192.168.25.3' : {'skl': [], 'suhu' : ()}}

def start():
    for x in DATA.keys():
        data_suhu = db.take_newest('dht', ['suhu', 'humidity'], x, ['ip'])
        DATA[x]['suhu'] = data_suhu
    for x in DATA.keys():
        data_skl = db.take_newest('skl', ['gpio', 'kondisi'], x, ['gpio','ip'])
        DATA[x]['skl'] = data_skl
    time.sleep(2)
st = up_thread(start)
st.join()

def take_data():
    global DATA, db
    while True:
        if STOP_THREAD:
            break
        for x in DATA.keys():
            data_suhu = db.take_newest('dht', ['suhu', 'humidity'], x, ['ip'])
            DATA[x]['suhu'] = data_suhu
        for x in DATA.keys():
            data_skl = db.take_newest('skl', ['gpio', 'kondisi'], x, ['gpio','ip'])
            DATA[x]['skl'] = data_skl
        time.sleep(2)
up_thread(take_data)

class ImageLampu(ttk.Frame):
    global db, STOP_THREAD, DATA

    def __init__(self,container, ip):
        super().__init__(container)
        self.gpio = [16,20,21,22]
        self.ip = ip
        self.label = {'6' : tk.Label(self),
                        '13' : tk.Label(self),
                        '19' : tk.Label(self),
                        '26' : tk.Label(self)}

        self.data = db.take_newest('skl', ['gpio', 'kondisi'], ip, grouping = ['gpio', 'ip'])

        self.img1 = (Image.open('img\lampu.png')).resize((50, 50), Image.ANTIALIAS)
        self.img2 = (Image.open('img\lampuon.png')).resize((50,50), Image.ANTIALIAS)
        self.on = ImageTk.PhotoImage(self.img2)
        self.off = ImageTk.PhotoImage(self.img1)

        self.__create_widget()
        self.after(100, lambda : up_thread_daemon(self.__configure))

    def __create_widget(self):
        self.label['6'].grid(column=0, row=0, padx=10, pady=2)
        self.label['13'].grid(column=1, row=0, padx=10, pady=2)
        self.label['19'].grid(column=2, row=0, padx=10, pady=2)
        self.label['26'].grid(column=3, row=0, padx=10, pady=2)
        self.__change_image()
        
    def __configure(self):
        while True:
            self.data = DATA[self.ip]['skl']
            self.__change_image()
            if STOP_THREAD:
                break
            time.sleep(3)

    def __change_image(self):
        for i in self.data:
            if i[1] == 1:
                self.label[str(i[0])].configure(image=self.on)
            elif i[1] == 0:
                self.label[str(i[0])].configure(image=self.off)
                
class Graphing(ttk.Frame):
    global a, f, db
    def __init__(self, container, connection) -> None:
        super().__init__()
        self.connection = connection
        canvas = FigureCanvasTkAgg(f, container)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=4,sticky='sw')

    def animate(self,i):
        data = db.take_data('dht')
        x = range(10)
        time_rasp = [str(x[3]) for x in data if x[-1] == '192.168.25.2'][-10:]
        time_rasp = [x[-8:-3] for x in time_rasp]
        a.clear()
        for addr in self.connection:
            suhu_rasp = [x[1] for x in data if x[-1] == addr][-10:]
            a.plot(x, suhu_rasp, 'o-', label = addr)
        a.set_xticks(x, time_rasp, rotation = 45)
        a.set_yticks(range(15,50))
        a.legend(loc = 4)

class LabelSuhu(ttk.Frame):
    global db, DATA, STOP_THREAD
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
        
        self.after(100, lambda : up_thread_daemon(self.__config))

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
            # data_suhu = db.take_data(table = 'dht', data = 'new', ip = self.ip)
            data_suhu = DATA[self.ip]['suhu']
            data_new = data_suhu[0]
            print(f"IP : {self.ip}")
            print(f"Data : {data_new}")
            text_humid = str(data_new[1])
            suhu = data_new[0]
            text = str(data_new[0])
            self.__change_color(suhu, text)
            self.humidity.configure(text=text_humid)
            if STOP_THREAD:
                break
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
        elif background=='gray':
            self.button = tk.Button(container, text = text, command=self.__command_on, bg=background, height='2', width='10')
        self.button.grid(row=grid[0], column=grid[1])

    ## Command untuk on or off
    def __command_on(self):
        clien.send(f'on {self.text} {self.ip}')
        self.button.configure(bg='green', command=self.__command_off)
    
    def __command_off(self):
        clien.send(f'off {self.text} {self.ip}')
        self.button.configure(bg='gray', command=self.__command_on)

class ButtonWidget(ttk.Frame):
    global db, Button_Name

    def __init__(self, container, ip):
        super().__init__(container, padding=20)
        self.ip = ip
        self.data = db.take_data(table = 'rly', data = 'all', ip=ip)
        self.button_collection = []
        self.__create_widget()

    def __create_widget(self):
        print(f"IP : {self.ip}")
        data = db.take_data('rly', ip= self.ip)[-8:]
        name = Button_Name[self.ip]

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
        for i in range(len(name)):
            condition = data[i][2]
            if condition == 0:
                ButtonToggle(self, column_row[i], name[i], 'green', self.ip)
            else:
                ButtonToggle(self, column_row[i], name[i], 'gray', self.ip)

class Tampilan(tk.Frame):

    def __init__(self, container, connected,text, ip):
        super().__init__(container, highlightbackground = 'black', width = '300', height = '300', pady = 30, highlightthickness=1)
        self.ip = ip
        self.text = text
        if connected:
            self.__create_widget()
        else:
            self.__not_connected()


    def __create_widget(self):
        tk.Label(self, text=self.text).grid(row=0, column=0)
        bt1 = ButtonWidget(self, self.ip)
        image = ImageLampu(self, self.ip)
        suhu = LabelSuhu(self, self.ip)
        bt1.grid(row=1, column=0)
        image.grid(row=2, column=0)
        suhu.grid(row=3, column=0)
 
    def __not_connected(self):
        ttk.Label(self, text=f"{self.ip} not connected").grid(row=0, column=0, padx=10)

class App(tk.Tk):
    global clien, IP, f
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        # self.resizable(0,0)
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
        tk.Button(self, text="EXIT", height=2, width=15,command=lambda:[clien.send("done"), self.kill_thread(),self.destroy()], bg='red', pady=10).grid(row=2, column=3, columnspan=2)
        
    def __listing_ip(self, file):
        with open(file, "r") as f:
            frame_text = []
            for x in f:
                if x[-1] == "\n":
                    x = x[:-1]
                line = x.split(" ")
                ip = line[-1]
                name = line[0]
                IP.append(ip)
                frame_text.append(name)
            return IP, frame_text
    
    def kill_thread(self):
        STOP_THREAD = TRUE
        time.sleep(5)
        return
    
app = App()
connection = [x for x in clien.connection if x != '192.168.25.1']
graph = Graphing(app, connection)
animate = animation.FuncAnimation(f, graph.animate, interval = 1000)
app.mainloop()
