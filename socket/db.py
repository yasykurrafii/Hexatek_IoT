import mysql.connector as mysql

class Database:

    def __init__(self, host = "localhost", user = "root", password = "admin"):
        self.host = host
        self.user = user
        self.password = password

        self.connect = mysql.connect(host = host, user = user, password = password, db = "hexatek")
        self.cursor = self.connect.cursor()
    
    def insert(self, command):
        try:
            self.cursor.execute(command)
            self.connect.commit()
        except :
            print("Command Salah")

    def take_data(self, command):
        self.cursor.execute(command)
        return self.cursor.fetchone()

# x = Database(password = "myr170500")
# x.execute("insert into hexatek.rly (gpio, kondisi) values (14, 1)")

