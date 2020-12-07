import json
import mysql.connector as mysql

class dboperation:
    def __init__(self):
        with open("passwd.json", "r") as passwd:
            self.credentials = json.load(passwd)

        self.db = mysql.connect(
                host = str(self.credentials["server"]),
                user = str(self.credentials["login"]),
                passwd = str(self.credentials["passwd"]),
                database = str(self.credentials["db"])
                )
        self.cursor = self.db.cursor()
        
    def insertbanned(self,data):
        query = "INSERT INTO `Aldous`(`acc_id`, `acc_link`, `acc_nick`, `date_of_detection`) VALUES (%s,%s,%s,%s)"
        self.cursor.executemany(query, data)
        self.db.commit()
    
    def db_banned(self):
        banned  = []
        query = "SELECT `acc_link` FROM `Aldous`"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        for x in records:
            banned.append(x[0])
        return banned 








