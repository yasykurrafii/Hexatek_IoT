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
        
    def stop(self):
        self.cursor.close()
        self.connect.close()

    def __restart_new(self):
        self.connect = mysql.connect(host = self.host, user = self.user, password = self.password, db = "hexatek")
        self.cursor = self.connect.cursor(buffered = True)
    
    def insert(self, command):
        self.__restart_new()
        try:
            self.cursor.execute(command)
            self.connect.commit()
            self.stop()
        except :
            print("Command Salah")
    
    def commands(self, command):
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        print(res)
        self.stop()
        return res

    def take_data(self, table, data = 'all', ip = ''):
        self.__restart_new()
        if ip != '':
            adr = self.command[ip]
            self.cursor.execute(f"Select * From {table} Where ip = '{ip}'")
        else:
            self.cursor.execute(f"SELECT * FROM {table}")
        try :
            res = ""
            if data == 'all':
                res = self.cursor.fetchall()
            elif data == 'new':
                res = self.cursor.fetchone()
            self.stop()
            return res
        except:
            raise "Choose data between New and All"

    def take_newest(self, tabel : str, res: list, ip:str, grouping : list = None):
        self.__restart_new()
        res = ','.join(res)
        group = ','.join(grouping)
        comm = f"SELECT {res} FROM {tabel} WHERE id IN (SELECT max(id) FROM {tabel} GROUP BY {group}) and ip = '{ip}';"
        self.cursor.execute(comm)
        res = self.cursor.fetchall()
        self.stop()
        time.sleep(1.5)
        return res


# x = Database(password = "myr170500")
# x.take_data('dht')

