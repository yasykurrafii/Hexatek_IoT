import mysql.connector as mysql
import time

from function import up_thread

class Database:

    def __init__(self, host = "localhost", user = "root", password = "admin"):
        self.host = host
        self.user = user
        self.password = password

        self.command = {'192.168.25.2' :('192.168.25.2',),
                        '192.168.25.3' : ('192.168.25.3',),
                        '192.168.25.4' : ('192.168.25.4',),
                        '192.168.25.5' : ('192.168.25.5',),
                        '192.168.25.6' : ('192.168.25.6',),}

        self.connect = mysql.connect(host = host, user = user, password = password, db = "hexatek")
        self.cursor = self.connect.cursor(buffered = True)

    def __restart_new(self):
        self.connect = mysql.connect(host = self.host, user = self.user, password = self.password, db = "hexatek")
        self.cursor = self.connect.cursor(buffered = True)
    
    def insert(self, command):
        self.__restart_new()
        try:
            self.cursor.execute(command)
            self.connect.commit()
        except :
            print("Command Salah")

    def take_data(self, table, data = 'all', ip = ''):
        self.__restart_new()
        if ip != '':
            adr = self.command[ip]
            self.cursor.execute(f"Select * From {table} Where ip = %s", adr)
        else:
            self.cursor.execute(f"SELECT * FROM {table}")
        try :
            if data == 'all':
                return self.cursor.fetchall()
            elif data == 'new':
                return self.cursor.fetchone()
            self.cursor.close()
        except:
            raise "Choose data between New and All"

    def take_gpio(self, ip, gpio):
        self.__restart_new()
        adr = self.command[ip]
        print(self.cursor.execute(f"SELECT * FROM rly WHERE ip = %s AND gpio = {gpio}", adr))
        return self.cursor.fetchall()

# x = Database(password = "myr170500")
# x.take_data('dht')

