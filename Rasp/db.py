import mysql.connector as mysql
import time
import function

# db = mysql.connect(host = '192.168.25.1', 
#             user = 'rasp1', 
#             password = 'rasp1',
#             db = 'hexatek')

# cursor = db.cursor()
# print(cursor)
# cursor.execute("""
# INSERT INTO dht(suhu, humidity, ip)
# VALUES (18, 1, '192.168.25.2')
# """)

# db.commit()
# print(cursor)

class Database:

    def __init__(self, host = 'localhost', user = 'root', password = 'admin'):
        self.host = host
        self.user = user
        self.password = password

        # Yasykur
        self.connect = mysql.connect(
            host = host, user = user, password = password, db = 'hexatek'
        )

        # Tera
        # self.connect = mysql.connect(
        #     host = host, user = user, password = password, db = 'hexatek', port=3360
        # )
        
        self.cursor = self.connect.cursor()

    def __restart_new(self):
        self.connect = mysql.connect(host = self.host, user = self.user, password = self.password, db = "hexatek")
        self.cursor = self.connect.cursor(buffered = True)

    def insert(self,command):
        self.__restart_new()
        self.cursor.execute(command)
        self.connect.commit()
        self.connect.close()
                