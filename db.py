import tkinter as tk
import mysql.connector as mysql
from tkinter import ttk

main = tk.Tk()
main.geometry("500x500")

## Start Connection
mydb = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "myr170500",
    db = "hexatek"
)

c = mydb.cursor()
c.execute("""SELECT * FROM dht""")
myresult = c.fetchall()
counter = 0

## End Connection

tree = ttk.Treeview(main, selectmode="browse")
## taro di grid(colum=3, row= 0 , columnspan = 2, rowspan= 2)
tree.grid(column=0, row=0)

tree["columns"]=("1", "2", "3")

tree['show'] = 'headings'

## Buat collumnya, lebar jangan di samain mintol anchornya boleh
tree.column("1", width = 30, anchor ='c')
tree.column("2", width = 90, anchor ='c')
tree.column("3", width = 90, anchor ='c')

## Untuk heading diatas
tree.heading("1", text = "id")
tree.heading("2", text = "date")    
tree.heading("3", text = "suhu")

## looping tapi belum bisa update baru karna harus pake while kayak kemaren
for row in myresult:
    tree.insert("", 'end', text = row[0],values =(row[0], row[1], row[2]))
    counter += 1 

main.mainloop()
## Jangan lupa 
## import mysql.connector 
## as mysql from tkinter import ttk