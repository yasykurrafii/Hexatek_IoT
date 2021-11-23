from logging import root
import tkinter as tk
from tkinter import Toplevel, ttk
from PIL import Image, ImageTk
import tkinter.font
from db import Database
from function import *

CONNECTION = []

class ButtonToggle(tk.Tk, Database):
    def __init__(self, container, row, column, ip, gpio, **kwargs):
        Database.__init__(self, password = 'myr170500')
        self.button = tk.Button(container, command = self.__command_on, **kwargs)
        self.button.grid(row = row, column=column, padx=2)
        self.orig_color = self.button.cget("bg")
        self.ip = ip
        self.gpio = gpio
        self.data = self.take_relay()
    
    def __command_on(self):
        # send(self.ip, "testing")
        self.button.configure(bg = "green", command = self.__command_off)

    def __command_off(self):
        self.button.configure(bg = self.orig_color,command = self.__command_on)

    def take_relay(self):
        data = super().take_gpio(self.ip, self.gpio)
        return data

# class Connecting(Database):
#     def __init__(self, ip):
#         Database().__init__(self, password='myr170500')
#         self.ip = ip
    
#     def take_data_dht(self):
#         super().take_


class Widget(tk.Tk, Database):
    def __init__(self, container, ip):
        self.container = container
        Database.__init__(self, password = 'myr170500')
        self.tree = ttk.Treeview(self.container, selectmode="browse")
        self.ip = ip
        self.data = {}
        self.stop = False

        self.img1 = (Image.open('img\lampu.png')).resize((50, 50), Image.ANTIALIAS)
        self.img2 = (Image.open('img\lampuon.png')).resize((50,50), Image.ANTIALIAS)
        self.on = ImageTk.PhotoImage(self.img2)
        self.off = ImageTk.PhotoImage(self.img1)

    def _all_data(self, ip = "127.0.0.1"):
        if ip == '127.0.0.1':
            dht = super().take_data(table = 'dht', data = 'all')[-10:]
        else:
            dht = super().take_data(table = 'dht', data = 'all', ip = ip)
        dht_new = dht[-1]
        suhu = dht_new[1]
        humid = dht_new[2]
        self.data = {'dht' : dht, 'suhu' : suhu, 'humid' : humid}
        time.sleep(10)

    def __build_label(self, text, row, column, columnspan, pady=0):
        font = tk.font.Font(family="Montserrat",size=12)
        tk.Label(self.container, text=text, font=font).grid(row=row, column=column, columnspan=columnspan, pady=pady)

    def __build_tabel(self, value, treeview):
        treeview['show'] = 'headings'
        for v in value['values']:
            treeview.column(v[0], width=v[1], anchor='c')
            treeview.heading(v[0], text=v[2])

    def __build_toplevel(self):
        toplevel = Toplevel(self.container)
        toplevel.title("DHT")
        tree = ttk.Treeview(toplevel, selectmode="browse")
        self.build_tree(tree)

    # Building Frame
    def build_frame(self):
        up_thread(self._all_data, self.ip)
        time.sleep(1)
        font = tk.font.Font(family="Montserrat",size=20)

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

        # Label
        tk.Label(self.container, text = "Frame", font = font).grid(column=0, row=0, columnspan=4)
        print(self.data['relay'])
        # Button
        for i in range(len(column_row)):
            column = column_row[i][0]
            row = column_row[i][1]
            ButtonToggle(self.container, column,row, self.ip, gpio[i], text = "Button", height="2", width="10")

        tk.Label(self.container, image= self.on).grid(row=3, column=0, pady=10, padx=2)
        tk.Label(self.container, image= self.off).grid(row=3, column=1, pady=10, padx=2)
        tk.Label(self.container, image= self.on).grid(row=3, column=2, pady=10, padx=2)
        tk.Label(self.container, image= self.off).grid(row=3, column=3, pady=10, padx=2)

        self.__build_label("Suhu", 4, 0, 2)
        self.__build_label(f"{self.data['suhu']} C", 5, 0, 2, 15)
        self.__build_label("Humidity", 4, 2, 2)
        self.__build_label(f"{self.data['humid']}%", 5, 2, 2, 15)

        logbut = tk.Button(self.container, text = "Checking Log", command=self.__build_toplevel)
        logbut.grid(row=6, column=1, columnspan=2, pady=5, ipadx=30)
    
    def build_tree(self, treeview):
        up_thread(self._all_data, self.ip)
        time.sleep(1)
        s = ttk.Style()
        s.configure("Treeview", rowheight = 50)
        counter = 0
        treeview['height'] = 10
        treeview.grid(column=0, row=0)
        value = {'values' : [("1", 30, "id"),
                            ("2", 150, "date"),
                            ("3", 110, "suhu"),
                            ("4", 110, "humid")]}

        treeview["columns"]=("1", "2", "3", "4")

        self.__build_tabel(value,treeview)

        ## looping tapi belum bisa update baru karna harus pake while kayak kemaren
        for row in self.data['dht']:
            treeview.insert("", 'end', text = row[0],values =(row[0], row[3], row[1], row[2]))
            counter += 1

    def not_connected(self):
        tk.Label(self.container, text = "Not Connected").grid(column=0, row=0, columnspan=4)


class Tampilan(tk.Frame, Widget):
    global CONNECTION

    # Belom ditambahin IP
    def __init__(self, container, row, column, ip = "127.0.0.1", treeview = False, columnspan = False, span = (0,0), **kwargs):
        self.kwarg = kwargs
        # self.connection = up_thread(self.checking_ip)
        try:
            self.pady = kwargs['pady']
            del self.kwarg['pady']
        except:
            pass
        super().__init__(container, highlightthickness=2, **self.kwarg)
        # Tambahin IP untuk Widgetnya
        Widget.__init__(self, self, ip)
        if ip not in CONNECTION and ip != "127.0.0.1":
            super().not_connected()
        else:
            if treeview:
                super().build_tree(self.tree)
            else:
                super().build_frame()
        if columnspan:
            self.grid(row=row, column=column, sticky="ew", padx=40, columnspan=span[0], rowspan=span[1])
        else:
            try:
                self.grid(row=row, column=column, padx=5, pady = self.pady)
            except:
                self.grid(row=row, column=column, padx=5)
    
    # def checking_ip(self):
    #     while not self.:
    #         self.connection = get_connection()
    #         time.sleep(1.0)

        

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        self.title("Page 1")
        self.connection = []
        self.stop = False

        up_thread(self.checking_ip)

        self.__create_widget()

        tk.Button(self, text="EXIT", height=2, width=15,command=lambda:[self.destroy(), self.stopped()], bg='red', pady=10).grid(row=2, column=3, columnspan=2)

    def __create_widget(self):
        # Ter ini udah ada grid nya jadi gausah lu pakein .grid lagi ya
        # Belom ditambahin IP, Lagi mikir gimana caranya
        frame  = Tampilan(self, 0,0, "192.168.25.2", highlightbackground = 'black', width = '300', height = '300', pady = 30)
        frame2 = Tampilan(self,0,1, "192.168.25.3", highlightbackground = 'black', width = '300', height = '300', pady = 30)
        frame3 = Tampilan(self, 0, 2, "192.168.25.4", highlightbackground = 'black', width = '300', height = '300', pady = 30)
        frame4 = Tampilan(self, 1, 0, "192.168.25.5", highlightbackground = 'black', width = '300', height = '300')
        frame5 = Tampilan(self, 1, 1, "192.168.25.6", highlightbackground = 'black', width = '300', height = '300')
        frame6 = Tampilan(self, 1, 2, "192.168.25.7", highlightbackground = 'black', width = '300', height = '300')
        tree1 = Tampilan(self, 0,3, treeview=True, columnspan=True, span=(2,2), width="500", height="500")

    def checking_ip(self):
        global CONNECTION
        while not self.stop:
            CONNECTION = get_connection()
            time.sleep(2)

    def stopped(self):
        self.stop = True

apl = GUI()
apl.mainloop()
