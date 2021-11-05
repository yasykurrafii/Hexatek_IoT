import tkinter as tk
from PIL import Image, ImageTk
from db import Database

class Widget(tk.Tk):
    def __init__(self, container):
        self.container = container

    def build_button(self, row, column, command = '', height="2", width="10"):
        tk.Button(self.container,text="Tombol",height=height, width=width).grid(row=row, column=column, padx=2)

    def build_label(self, text, row, column, columnspan, pady=0):
        tk.Label(self.container, text=text).grid(row=row, column=column, columnspan=columnspan, pady=pady)
    
    def __call__(self):
        self.img1 = (Image.open('img\lampu.png')).resize((50, 50), Image.ANTIALIAS)
        self.img2 = (Image.open('img\lampuon.png')).resize((50,50), Image.ANTIALIAS)
        self.on = ImageTk.PhotoImage(self.img2)
        self.off = ImageTk.PhotoImage(self.img1)

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
            self.build_button(i[0],i[1])

        tk.Label(self.container, image= self.on).grid(row=3, column=0, pady=10, padx=2)
        tk.Label(self.container, image= self.off).grid(row=3, column=1, pady=10, padx=2)
        tk.Label(self.container, image= self.on).grid(row=3, column=2, pady=10, padx=2)
        tk.Label(self.container, image= self.off).grid(row=3, column=3, pady=10, padx=2)

        self.build_label("Suhu", 4, 0, 2)
        self.build_label("27 C", 5, 0, 2, 15)
        self.build_label("Humidity", 4, 2, 2)
        self.build_label("70%", 5, 2, 2, 15)


class Tampilan(tk.Frame):
    # db = Database()
    def __init__(self, container, row, column, color = 'black', width = '300', height = '300' ):
        super().__init__(container, highlightbackground=color, width=width, height=height, highlightthickness=2)
        self.grid(row=row, column=column, pady=2, padx=5)
        widget = Widget(self)
        widget()
        

        


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        self.title("Page 1")

        self.__create_widget()

        tk.Button(self, text="EXIT", height=2, width=15,command=self.destroy).grid(row=3, column=2, pady=150)

    def __create_widget(self):
        frame = Tampilan(self,0,0)
        frame.grid(row=0, column=0)
        frame2 = Tampilan(self,0,1)
        frame2.grid(row=0, column=1)

app = App()
app.mainloop()