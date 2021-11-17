import mysql.connector as mysql

class Database:

    def __init__(self, host = "localhost", user = "root", password = "admin"):
        self.host = host
        self.user = user
        self.password = password

        self.connect = mysql.connect(host = host, user = user, password = password, db = "hexatek")
        self.cursor = self.connect.cursor(buffered = True)
    
    def insert(self, command):
        try:
            self.cursor.execute(command)
            self.connect.commit()
        except :
            print("Command Salah")

    def take_data(self, table, data = 'all', ip = ''):
        if ip != '':
            command = {'192.168.25.2' :('192.168.25.2',),
                        '192.168.25.3' : ('192.168.25.3',),
                        '192.168.25.4' : ('192.168.25.4',),
                        '192.168.25.5' : ('192.168.25.5',),
                        '192.168.25.6' : ('192.168.25.6',),}
            adr = command[ip]
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

# x = Database(password = "myr170500")
# x.take_data('dht')

