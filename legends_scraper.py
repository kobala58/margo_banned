import discord
from discord.ext import commands
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector
from mysql.connector import Error
import re
import datetime
from database_handle import dboperation


chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--headless')

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

def getinfo(link):
    db = dboperation()
    legi = []
    #base = "https://www.margonem.pl/"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    postki = soup.find_all('div' , class_="inside_char")
    for x in postki:
        browser = webdriver.Chrome(options=chrome_options)
        world = x.find(class_='inside_char_avatar')["c_world"]
        if world != "Aldous":
            continue
        a = x.find('a')['href']
        z = x.find(class_='inside_char_stats')
        z = z.find('b')
        nick = z.text
        browser.get(link+a)
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        soup2 = soup2.find(id = "tab1_content")
        items = soup2.find_all(class_ = "itemborder")
        for xx in items:
            z = xx.find("img")["tip"]
            soup3 = BeautifulSoup(z, 'html.parser')
            name = soup3.find("b").text
            item = soup3.find(class_ = "legendary")
            who = soup3.find(class_ = "looter")
            id_konto = re.sub("\D", "", link)
            if item is not None:
                try:
                    legi.append((id_konto,nick,name,who.text))
                except AttributeError:
                    legi.append((id_konto,nick,name,"CRAFTED"))
        browser.close()
    if legi:
        db.lega(legi)
    

def banned():
    seen = set()
    for x in range(43,100):
        link = "https://www.margonem.pl/?task=ranking&w=aldous&p="+str(x)
        a = get_plyers(link)
        print("Start {} page".format(x))
        for z in a:
            if z[0] not in seen:
                    seen.add(z[0])
                    id_konto = re.sub("\D", "", z[0])
                    getinfo("https://www.margonem.pl/"+z[0])

print("Start: {}".format(datetime.datetime.now()))
banned()
print("End: {}".format(datetime.datetime.now()))
