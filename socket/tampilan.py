import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.attributes('-fullscreen', True)
root.resizable(False, False)
root.title("Page 1")

img1 = (Image.open('img\lampu.png')).resize((50, 50), Image.ANTIALIAS)
img2 = (Image.open('img\lampuon.png')).resize((50,50), Image.ANTIALIAS)
on = ImageTk.PhotoImage(img2)
off = ImageTk.PhotoImage(img1)

frame1 = tk.Frame(root, width="300", height="300", bg="black")
frame1.grid(row=0, column=0, pady=2, padx=5)
frame2 = tk.Frame(root, width="300", height="300", highlightbackground="black", highlightthickness=2)
frame2.grid(row=1, column=0, pady=2, padx=5)
frame3 = tk.Frame(root, width="300", height="300", bg="green")
frame3.grid(row=0, column=1, pady=2, padx=2)
frame4 = tk.Frame(root, width="300", height="300", bg="yellow")
frame4.grid(row=1, column=1, pady=2, padx=2)
frame5 = tk.Frame(root, width="300", height="300", bg="pink")
frame5.grid(row=0, column=2, pady=2, padx=2)
frame6 = tk.Frame(root, width="300", height="300", bg="blue")
frame6.grid(row=1, column=2, pady=2, padx=2)

#########       FRAME1          ##########  
jframe1 = tk.Label(frame1, text="FRAME 1")
jframe1.grid(row=0, column=0, columnspan=4, pady=5)

tombol1 = tk.Button(frame1, text="Tombol",height=2, width=10)
tombol1.grid(row=1, column=0, padx=2, pady=5)

tombol2 = tk.Button(frame1,text="Tombol",height=2, width=10)
tombol2.grid(row=1, column=1, padx=2)

tombol3 = tk.Button(frame1,text="Tombol",height=2, width=10)
tombol3.grid(row=1, column=2, padx=2)

tombol8 = tk.Button(frame1,text="Tombol",height=2, width=10)
tombol8.grid(row=1, column=3, padx=2)

tombol4 = tk.Button(frame1,text="Tombol",height=2, width=10)
tombol4.grid(row=2, column=0, padx=2)

tombol5 = tk.Button(frame1,text="Tombol",height=2, width=10)
tombol5.grid(row=2, column=1, padx=2)

tombol6 = tk.Button(frame1,text="Tombol",height=2, width=10)
tombol6.grid(row=2, column=2, padx=2)

tombol7 = tk.Button(frame1,text="Tombol",height=2, width=10)
tombol7.grid(row=2, column=3, padx=2)

kosong = tk.Label(frame1, bg="grey")
kosong.grid(row=3, column=0, columnspan=4, pady=20, sticky="ew")

jsuhu = tk.Label(frame1, text="SUHU")
jsuhu.grid(row=4, column=0, columnspan=2)

suhu = tk.Label(frame1, text="27 C")
suhu.grid(row=5, column=0, columnspan=2, pady=15)

jhum = tk.Label(frame1, text="HUMIDITY")
jhum.grid(row=4, column=2, columnspan=2)

humid = tk.Label(frame1, text="70%")
humid.grid(row=5, column=2, columnspan=2, pady=15)

#########       FRAME 2         ##########  
jframe2 = tk.Label(frame2, text="FRAME 2")
jframe2.grid(row=0, column=0, columnspan=4, pady=5)

tombol1 = tk.Button(frame2, text="Tombol",height=2, width=10)
tombol1.grid(row=1, column=0, padx=2, pady=5)

tombol2 = tk.Button(frame2,text="Tombol",height=2, width=10)
tombol2.grid(row=1, column=1, padx=2)

tombol3 = tk.Button(frame2,text="Tombol",height=2, width=10)
tombol3.grid(row=1, column=2, padx=2)

tombol8 = tk.Button(frame2,text="Tombol",height=2, width=10)
tombol8.grid(row=1, column=3, padx=2)

tombol4 = tk.Button(frame2,text="Tombol",height=2, width=10)
tombol4.grid(row=2, column=0, padx=2)

tombol5 = tk.Button(frame2,text="Tombol",height=2, width=10)
tombol5.grid(row=2, column=1, padx=2)

tombol6 = tk.Button(frame2,text="Tombol",height=2, width=10)
tombol6.grid(row=2, column=2, padx=2)

tombol7 = tk.Button(frame2,text="Tombol",height=2, width=10)
tombol7.grid(row=2, column=3, padx=2)


########        Sensor          #########
lampu1 = tk.Label(frame2, image= on)
lampu1.grid(row=3, column=0, pady=10, padx=2)
lampu2 = tk.Label(frame2, image= off)
lampu2.grid(row=3, column=1, pady=10, padx=2)
lampu3 = tk.Label(frame2, image= on)
lampu3.grid(row=3, column=2, pady=10, padx=2)
lampu4 = tk.Label(frame2, image= off)
lampu4.grid(row=3, column=3, pady=10, padx=2)

########        Space           #########
kosong = tk.Label(frame2, bg="grey")
kosong.grid(row=4, column=0, columnspan=4, pady=10, sticky="ew")
#########       DHTGRID         #########
jsuhu = tk.Label(frame2, text="SUHU")
jsuhu.grid(row=5, column=0, columnspan=2)
suhu = tk.Label(frame2, text="27 C")
suhu.grid(row=6, column=0, columnspan=2, pady=15)
jhum = tk.Label(frame2, text="HUMIDITY")
jhum.grid(row=5, column=2, columnspan=2)
humid = tk.Label(frame2, text="70%")
humid.grid(row=6, column=2, columnspan=2, pady=15)


exit = tk.Button(root, text="EXIT", height=2, width=15,command=root.destroy)
exit.grid(row=3, column=2, pady=150)
root.mainloop()