import json
import mysql.connector as mysql
from discord_webhook import DiscordWebhook

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
    
    def add_player(self,data):
        query = "INSERT INTO `Gracze`(`eq_id`, `eq_name`, `eq_lvl`, `eq_prof`, `acc_id`, `clan_name`, `clan_id`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.executemany(query, data)
        except:
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/789054968144986112/xWYpVPmkuL9ODCZrsOk8HThp52Cud1gSHNL_qt8oetvadIRe8XmGHW-7ZkMVRvPZ_yjH', content='Błąd w tym secie danych \n ````\n {} ```'.format(data))
            webhook.execute()
        self.db.commit()

    def lid(self,data):
        lids = []
        query = "SELECT Gracze.eq_name FROM Gracze INNER JOIN Gracze_copy ON Gracze.acc_id = Gracze_copy.acc_id"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        for x in records:
            lids.append(x[0])
        return lids 
    
    def lega(self,data):
        query = "INSERT INTO leguwy(konto_id,nazwa_postaci,lega_nazwa,opis) VALUES (%s,%s,%s,%s)"
        try:
            self.cursor.executemany(query, data)
        except:
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/789054968144986112/xWYpVPmkuL9ODCZrsOk8HThp52Cud1gSHNL_qt8oetvadIRe8XmGHW-7ZkMVRvPZ_yjH', content='Błąd w tym secie danych \n ````\n {} ```'.format(data))
            webhook.execute()
        self.db.commit()


