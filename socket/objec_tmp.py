import tkinter as tk
import tkinter.font
from PIL import Image, ImageTk
from db import Database
# from gui import up_thread

class ButtonToggle(tk.Tk):
    def __init__(self, container, row, column, text = "Button", height="2", width="10"):
        self.button = tk.Button(container, text = text, height=height, width=width, command = self.__command)
        self.button.grid(row = row, column=column, padx=2)
    
    def __command(self):
        self.button.configure(bg = "green")

class Widget(tk.Tk, Database):
    def __init__(self, container):
        self.container = container
        Database.__init__(self, password = 'myr170500')
        self.dht = super().take_data(table = 'dht', data = 'new')
        self.suhu = self.dht[1]
        self.humid = self.dht[2]

        self.img1 = (Image.open('img\lampu.png')).resize((50, 50), Image.ANTIALIAS)
        self.img2 = (Image.open('img\lampuon.png')).resize((50,50), Image.ANTIALIAS)
        self.on = ImageTk.PhotoImage(self.img2)
        self.off = ImageTk.PhotoImage(self.img1)

    def __build_label(self, text, row, column, columnspan, pady=0):
        tk.Label(self.container, text=text).grid(row=row, column=column, columnspan=columnspan, pady=pady)

    def __button_on(self):
        print("Button on")


    # Building Frame
    def build_frame(self):
        
        font1 = tk.font.Font(family="Montserrat",size=20)
        font2 = tk.font.Font(family="Montserrat",size=12)

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
        tk.Label(self.container, text = "Frame").grid(column=0, row=0, columnspan=4)

        # Button
        for i in self.column_row:
            ButtonToggle(self.container, i[0],i[1])

        tk.Label(self.container, image= self.on).grid(row=3, column=0, pady=10, padx=2)
        tk.Label(self.container, image= self.off).grid(row=3, column=1, pady=10, padx=2)
        tk.Label(self.container, image= self.on).grid(row=3, column=2, pady=10, padx=2)
        tk.Label(self.container, image= self.off).grid(row=3, column=3, pady=10, padx=2)

        self.__build_label("Suhu", 4, 0, 2)
        self.__build_label(f"{self.suhu} C", 5, 0, 2, 15)
        self.__build_label("Humidity", 4, 2, 2)
        self.__build_label(f"{self.humid}%", 5, 2, 2, 15)
    
    # def build_tree(self):

class Tampilan(tk.Frame, Widget):

    # Belom ditambahin IP
    def __init__(self, container, row, column,   color = 'black', width = '300', height = '300'):
        super().__init__(container, highlightbackground=color, width=width, height=height, highlightthickness=2)
        # Tambahin IP untuk Widgetnya
        Widget.__init__(self, self)
        super().build_frame()
        self.grid(row=row, column=column, pady=2, padx=5)

        

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        self.title("Page 1")

        self.__create_widget()

        tk.Button(self, text="EXIT", height=2, width=15,command=self.destroy).grid(row=3, column=3)

    def __create_widget(self):
        # Ter ini udah ada grid nya jadi gausah lu pakein .grid lagi ya
        # Belom ditambahin IP, Lagi mikir gimana caranya
        frame  = Tampilan(self,0,0)
        frame2 = Tampilan(self,0,1)
        frame3 = Tampilan(self, 0, 2)
        frame4 = Tampilan(self, 1, 0)
        frame5 = Tampilan(self, 1, 1)
        frame6 = Tampilan(self, 1, 2)

app = App()
app.mainloop()
