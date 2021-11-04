import tkinter as tk
import tkinter.font
from PIL import Image, ImageTk

class Tampilan(tk.Frame):
    def __init__(self, container, row, column, color = 'black'):
        super().__init__(container, highlightbackground=color, highlightthickness=2)

        self.img1 = (Image.open('img\lampu.png')).resize((50, 50), Image.ANTIALIAS)
        self.img2 = (Image.open('img\lampuon.png')).resize((50,50), Image.ANTIALIAS)
        self.on = ImageTk.PhotoImage(self.img2)
        self.off = ImageTk.PhotoImage(self.img1)
        font1 = tk.font.Font(family="Montserrat",size=20)
        font2 = tk.font.Font(family="Montserrat",size=12)

        self.grid(row=row, column=column, pady=2, padx=5)

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
        tk.Label(self, text = "Location").grid(column=0, row=0, columnspan=4, pady=5)

        # Button
        for i in self.column_row:
            self.build_button(i[0],i[1])

        tk.Label(self, image= self.on).grid(row=3, column=0, pady=10, padx=2)
        tk.Label(self, image= self.off).grid(row=3, column=1, pady=10, padx=2)
        tk.Label(self, image= self.on).grid(row=3, column=2, pady=10, padx=2)
        tk.Label(self, image= self.off).grid(row=3, column=3, pady=10, padx=2)

        tk.Label(self, text="Sensors 1").grid(row=4, column=0, pady=15)
        tk.Label(self, text="Sensors 2").grid(row=4, column=1, pady=15)
        tk.Label(self, text="Sensors 3").grid(row=4, column=2, pady=15)
        tk.Label(self, text="Sensors 4").grid(row=4, column=3)

        tk.Label(self, text="Temperature").grid(row=5, column=0, columnspan=2)

        tk.Label(self, text="27 C").grid(row=6, column=0, columnspan=2, pady=15

        tk.Label(self, text="HUMIDITY").grid(row=5, column=2, columnspan=2)

        tk.Label(self, text="70%").grid(row=6, column=2, columnspan=2, pady=15)

    def build_button(self, row, column, command = '', height="2", width="10"):
        tk.Button(self,text="Control",height=height, width=width).grid(row=row, column=column, padx=2)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        self.title("Page 1")

        self.__create_widget()

        tk.Button(self, text="EXIT", height=2, width=15,command=self.destroy).grid(row=3, column=3)

    def __create_widget(self):
        frame  = Tampilan(self,0,0).grid(row=0, column=0)
        frame2 = Tampilan(self,0,1).grid(row=0, column=1)
        frame3 = Tampilan(self, 0, 2).grid(row=0, column=2)
        frame4 = Tampilan(self, 1, 0).grid(row=1, column=0)
        frame5 = Tampilan(self, 1, 1).grid(row=1, column=1)
        frame6 = Tampilan(self, 1, 2).grid(row=1, column=2)

app = App()
app.mainloop()
