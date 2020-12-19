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

def inside_info(link,id):
    #base = "https://www.margonem.pl/"
    db = dboperation()
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    postki = soup.find_all('div' , class_="inside_char")
    data = []
    for x in postki:
        world = x.find(class_='inside_char_avatar')["c_world"]
        if world != "Aldous":
            continue
        z = x.find(class_='inside_char_stats')
        nick = z.find('b')
        nick = nick.text
        clanlink = z.find("a",href = True)
        try:
            clan_id = clanlink["href"]
            clan_name = clanlink.text
        except:
            clan_id = "Brak"
            clan_name = "Brak"
        full = (x.find(class_='inside_char_avatar')["c_id"],nick,x.find(class_='inside_char_avatar')["c_lvl"],x.find(class_='inside_char_avatar')["c_prof"],id,clan_name,clan_id)
        data.append(full)
    db.add_player(data)
    

def banned():
    seen = set()
    for x in range(0,100):
        link = "https://www.margonem.pl/?task=ranking&w=aldous&p="+str(x)
        a = get_plyers(link)
        print("Start {} page".format(x))
        for z in a:
            if z[0] not in seen:
                    seen.add(z[0])
                    id_konto = re.sub("\D", "", z[0])
                    inside_info("https://www.margonem.pl/"+z[0],id_konto)

banned()