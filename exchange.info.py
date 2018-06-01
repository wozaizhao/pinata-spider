import requests
import bs4
import datetime
import time
import re
from peewee import *

#db = SqliteDatabase('./exchange.db')

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')

class ExchangeInfo(Model):
    rank = IntegerField()
    name = CharField()
    url = CharField()
    fees = CharField()
    chat = CharField()
    blog = CharField()
    twitter = CharField()
    alive = BooleanField(default=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

db.connect()

if not ExchangeInfo.table_exists():
  db.create_tables([ExchangeInfo])

response = requests.get('https://coinmarketcap.com/exchanges/volume/24-hour/')

soup = bs4.BeautifulSoup(response.text,"html.parser")

html = soup.select('.volume-header a')

for index,item in enumerate(html):

    link = "https://coinmarketcap.com" + item.attrs['href']
    time.sleep(3)
    subpage = requests.get(link)

    subsoup = bs4.BeautifulSoup(subpage.text,"html.parser")

    nameobj = subsoup.select('.text-large')
    name = nameobj[0].text.strip()

    urlobj = subsoup.select('.col-xs-12 .list-unstyled a')

    fees = ''
    chat = ''
    blog = ''
    url = ''
    twitter = ''

    for i,item in enumerate(urlobj):
        text = item.text
        href = item.attrs['href']

        if re.match(r"http", text):
            url = href
        if re.match(r"Fees", text):
            fees = href
        if re.match(r"Chat", text):
            chat = href
        if re.match(r"Blog", text):
            blog = href  
        if re.match(r"@", text):
            twitter = href            
    
    exchangeinfo = ExchangeInfo(rank=index+1,name=name,fees=fees,chat=chat,blog=blog,url=url,twitter=twitter)
    exchangeinfo.save()

db.close()

