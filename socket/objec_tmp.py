import tkinter as tk
from tkinter import Toplevel, ttk
from PIL import Image, ImageTk
from db import Database
from rasp_con import get_connection

class ButtonToggle(tk.Tk):
    def __init__(self, container, row, column, **kwargs):
        self.button = tk.Button(container, command = self.__command_on, **kwargs)
        self.button.grid(row = row, column=column, padx=2)
        self.orig_color = self.button.cget("bg")
    
    def __command_on(self):
        self.button.configure(bg = "green", command = self.__command_off)

    def __command_off(self):
        self.button.configure(bg = self.orig_color,command = self.__command_on)

# class Connecting(Database):
#     def __init__(self, ip):
#         Database().__init__(self, password='myr170500')
#         self.ip = ip
    
#     def take_data_dht(self):
#         super().take_


class Widget(tk.Tk, Database):
    def __init__(self, container):
        self.container = container
        Database.__init__(self, password = 'myr170500')
        self.dht = super().take_data(table = 'dht', data = 'all')
        self.dht_new = self.dht[-1]
        self.tree = ttk.Treeview(self.container, selectmode="browse")
        self.suhu = self.dht_new[1]
        self.humid = self.dht_new[2]

        self.img1 = (Image.open('img\lampu.png')).resize((50, 50), Image.ANTIALIAS)
        self.img2 = (Image.open('img\lampuon.png')).resize((50,50), Image.ANTIALIAS)
        self.on = ImageTk.PhotoImage(self.img2)
        self.off = ImageTk.PhotoImage(self.img1)

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
        
        font = tk.font.Font(family="Montserrat",size=20)

        self.column_row = [
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

        # Button
        for i in self.column_row:
            ButtonToggle(self.container, i[0],i[1],text = "Button", height="2", width="10")

        tk.Label(self.container, image= self.on).grid(row=3, column=0, pady=10, padx=2)
        tk.Label(self.container, image= self.off).grid(row=3, column=1, pady=10, padx=2)
        tk.Label(self.container, image= self.on).grid(row=3, column=2, pady=10, padx=2)
        tk.Label(self.container, image= self.off).grid(row=3, column=3, pady=10, padx=2)

        self.__build_label("Suhu", 4, 0, 2)
        self.__build_label(f"{self.suhu} C", 5, 0, 2, 15)
        self.__build_label("Humidity", 4, 2, 2)
        self.__build_label(f"{self.humid}%", 5, 2, 2, 15)

        logbut = tk.Button(self.container, text = "Checking Log", command=self.__build_toplevel)
        logbut.grid(row=6, column=1, columnspan=2, pady=5, ipadx=30)
    
    def build_tree(self, treeview):
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
        for row in self.dht:
            treeview.insert("", 'end', text = row[0],values =(row[0], row[3], row[1], row[2]))
            counter += 1 


class Tampilan(tk.Frame, Widget):

    # Belom ditambahin IP
    def __init__(self, container, row, column, treeview = False, columnspan = False, span = (0,0), **kwargs):
        self.kwarg = kwargs
        try:
            self.pady = kwargs['pady']
            del self.kwarg['pady']
        except:
            pass
        super().__init__(container, highlightthickness=2, **self.kwarg)
        # Tambahin IP untuk Widgetnya
        Widget.__init__(self, self)
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

        

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        self.title("Page 1")
        self.connection = get_connection()

        self.__create_widget()

        tk.Button(self, text="EXIT", height=2, width=15,command=self.destroy, bg='red', pady=10).grid(row=2, column=3, columnspan=2)

    def __create_widget(self):
        # Ter ini udah ada grid nya jadi gausah lu pakein .grid lagi ya
        # Belom ditambahin IP, Lagi mikir gimana caranya
        frame  = Tampilan(self,0,0,highlightbackground = 'black', width = '300', height = '300', pady = 30)
        frame2 = Tampilan(self,0,1,highlightbackground = 'black', width = '300', height = '300', pady = 30)
        frame3 = Tampilan(self, 0, 2,highlightbackground = 'black', width = '300', height = '300', pady = 30)
        frame4 = Tampilan(self, 1, 0,highlightbackground = 'black', width = '300', height = '300')
        frame5 = Tampilan(self, 1, 1,highlightbackground = 'black', width = '300', height = '300')
        frame6 = Tampilan(self, 1, 2,highlightbackground = 'black', width = '300', height = '300')
        tree1 = Tampilan(self, 0,3, treeview=True, columnspan=True, span=(2,2), width="500", height="500")

apl = App()
apl.mainloop()
