import mysql.connector as mysql

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

        self.connect = mysql.connect(
            host = host, user = user, password = password, db = 'hexatek'
        )
        self.cursor = self.connect.cursor()

    def insert(self, command):
        self.cursor.execute(command)
        self.connect.commit()
        print("Berhasil masukin data")