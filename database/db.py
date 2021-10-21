import mysql.connector as mysql

class Database:

    def __init__(self, host = "localhost", user = "root", password = "admin"):
        self.host = host
        self.user = user
        self.password = password

        self.connect = mysql.connect(host = host, user = user, password = password)
        self.cursor = self.connect.cursor()
    
    def execute(self, command):
        try:
            self.cursor.execute(command)
            self.connect.commit()
        except :
            print("Command Salah")

x = Database(password = "myr170500")
x.execute("insert into hexatek.dht (suhu, humidity) values (19.0, 60.0)")

