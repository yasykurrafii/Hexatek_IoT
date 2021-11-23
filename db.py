import mysql.connector as mysql

db = mysql.connect(host = 'localhost', user = 'root', password = 'myr170500', db = "hexatek")

print(db)