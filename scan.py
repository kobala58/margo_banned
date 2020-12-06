import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import asyncio
from discord_webhook import DiscordWebhook
import database_handle



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
    banned_list = []
    for x in range(0,100):
        link = "https://www.margonem.pl/?task=ranking&w=aldous&p="+str(x)
        a = get_plyers(link)
        for z in a:
            if z[0] not in seen:
                page = requests.get("https://www.margonem.pl/"+z[0])
                soup = BeautifulSoup(page.content, 'html.parser')
                is_ban = soup.find('p',id="info").text
                if str(is_ban.strip()) == "Konto zablokowane":
                    seen.add(z[0])
                    banned_list.append(z)
    return banned_list

def banned_klan(link: str):
    seen = set() 
    a = get_plyers(link)
    for z in a:
        if z[0] not in seen:
            page = requests.get("https://www.margonem.pl/"+z[0])
            soup = BeautifulSoup(page.content, 'html.parser')
            is_ban = soup.find('p',id="info").text
            if str(is_ban.strip()) == "Konto zablokowane":
                seen.add(z[0])
                print(z[1])
    print("Koniec zbanowanych kont")

banned()
