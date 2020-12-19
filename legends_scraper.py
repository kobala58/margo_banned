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


chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--headless')


def getinfo(link):
    #base = "https://www.margonem.pl/"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    postki = soup.find_all('div' , class_="inside_char")
    browser = webdriver.Chrome(options=chrome_options)
    for x in postki:
        #print(x.find(class_='inside_char_avatar')["c_lvl"])
        world = x.find(class_='inside_char_avatar')["c_world"]
        if world != "Aldous":
            continue
        a = x.find('a')['href']
        z = x.find(class_='inside_char_stats')
        z = z.find('b')
        nick = z.text
        print(link+a)
        browser.get(link+a)
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        soup2 = soup2.find(id = "tab1_content")
        items = soup2.find_all(class_ = "itemborder")
        for xx in items:
            z = xx.find("img")["tip"]
            soup = BeautifulSoup(z, 'html.parser')
            name = soup.find("b").text
            item = soup.find(class_ = "legendary")
            who = soup.find(class_ = "looter")
            id_konto = re.sub("\D", "", link)
            if item is not None:
                try:
                    print(id_konto,"/",nick,"/",name,"/",who.text)
                except AttributeError:
                    print(id_konto,"/",nick,"/",name,"/","CRAFTED")
    browser.close()    
    


getinfo("https://www.margonem.pl/?task=profile&id=1157217")

