from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

cmc = requests.get('https://coinmarketcap.com/')
soup = BeautifulSoup(cmc.content, 'html.parser')

#Inspect different tags of the page
print(soup.title)
print(soup.h1)
print(soup.h3)

#Print the col names from the main page
content = soup.find('div', {"class": "Box-sc-16r8icm-0 quq9zv-0 lejKzT"})
for i in content.findAll('a'):
    print(i.text)

#Print change of the market cap from the top div
content = soup.find('div', {"class": "Box-sc-16r8icm-0 ioCTcw"})
for i in content.findAll('p'):
    print(i.text)

#Print the main table's col names from thead tag
content = soup.find('thead', {"class": "rc-table-thead"})
for i in content.findAll('p'):
    print(i.text)
    
#List all the available rows     
content = soup.find("tbody")
for i in content.findAll('p'):
    print(i.text)

#Return browser-like version of the page to narrow the search
print(soup.prettify())

#Narrow the search domain
page_data = soup.find('script', id='__NEXT_DATA__', type="application/json")

#Save all the rows in the JSON format
coin_data = json.loads(page_data.contents[0]) #.contents[0] removes 'script' tags

#Create the list of dicts that contains only coins data
coin_list = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

#Create a dict {'coin ID': 'coin name'}
coins = {}
for i in coin_list:
    coins[str(i['id'])] = i['slug']

#Save vals to the list    
    coins_l = list(coins.values())
for i in coins_l:
    print(str(i))
    
#Check status for 10 coins (10 = limit of requests)
ten_coins = coins_l[0:10]
for i in ten_coins:
    print(requests.get('https://coinmarketcap.com/currencies/' + i 
                        + '/historical-data/?start=20130429&end=20201022').status_code)

#Extract historical data
#Only bitcoin
page = requests.get('https://coinmarketcap.com/currencies/'+
                        'bitcoin/historical-data/?start=20130429&end=20201022')
#Try dfnt parsers (lxml or html.parser)
soup = BeautifulSoup(page.text, 'lxml')

#Parsing the table
data = []
table_body = soup.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [x.text.strip() for x in cols]
    data.append([x for x in cols if x])

#Create df
btc = pd.DataFrame(data, columns = ['Date', 'Open*', 'High', 'Low', 'Close**', 'Volume', 'Market Cap'])

    
