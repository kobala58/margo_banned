import requests
from bs4 import BeautifulSoup
import asyncio
from discord_webhook import DiscordWebhook
from database_handle import dboperation
import re
from datetime import date

def get_players(link):
    page = requests.get(link)  
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('tr', class_='row0')
    res2 = soup.find_all('tr', class_='row1')
    wff = results + res2
    z = []
    print(wff[-1].text)
    for x in wff:
        pass
        #print(x.text)
        #test = x.find_all(class_="cen")
        #for z in test:
            #print(z.text)

#get_players("https://www.margonem.pl/?task=clanpage&id=139&w=aldous")
        
            