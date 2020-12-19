import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import asyncio
from discord_webhook import DiscordWebhook
from database_handle import dboperation
import re
from datetime import date
from discord_webhook import DiscordWebhook

def get_plyers(link):
    page = requests.get(link)  
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('tr', class_='row0')
    res2 = soup.find_all('tr', class_='row1')
    wff = results + res2
    z = []
    for postki in wff:
        a = [postki.find('a')['href'],postki.find('a').text]
        z.append(a)
    return z

def banned():
    seen = set()
    now = date.today()
    today = now.strftime("%Y-%m-%d")
    for x in range(0,100):
        db = dboperation()
        link = "https://www.margonem.pl/?task=ranking&w=aldous&p="+str(x)
        a = get_plyers(link)
        banned_list = []
        print("Start {} page".format(x))
        for z in a:
            if z[0] not in seen:
                page = requests.get("https://www.margonem.pl/"+z[0])
                soup = BeautifulSoup(page.content, 'html.parser')
                is_ban = soup.find('p',id="info").text
                if str(is_ban.strip()) == "Konto zablokowane":
                    seen.add(z[0])
                    id_konto = re.sub("\D", "", z[0])
                    tr = (id_konto,z[0],z[1],today)
                    banned_list.append(tr)
        print("Started inserting...")
        db.insertbanned(banned_list)
        
            
    return banned_list

def new_bans():
    db = dboperation()
    banned = db.db_banned()
    seen = set(banned)
    now = date.today()
    today = now.strftime("%Y-%m-%d")
    for x in range(0,100):
        link = "https://www.margonem.pl/?task=ranking&w=aldous&p="+str(x)
        a = get_plyers(link)
        banned_list = []
        print("Start {} page".format(x))
        for z in a:
            if z[0] not in seen:
                page = requests.get("https://www.margonem.pl/"+z[0])
                soup = BeautifulSoup(page.content, 'html.parser')
                is_ban = soup.find('p',id="info").text
                if str(is_ban.strip()) == "Konto zablokowane":
                    seen.add(z[0])
                    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/785516123515781130/LnBJT1OCStYQ0y8CZz3Hw-ebvj7tTJm0w8tyMBNdwlzvrkER9rVAWgNjDDhfEAsmNx5O', content='{}: https://www.margonem.pl/{}'.format(z[1],z[0]))
                    response = webhook.execute()
                    id_konto = re.sub("\D", "", z[0])
                    tr = (id_konto,z[0],z[1],today)
                    banned_list.append(tr)
        print("Started inserting...")
        db.insertbanned(banned_list)
    
new_bans()