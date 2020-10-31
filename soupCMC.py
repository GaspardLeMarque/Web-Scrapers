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

#Extract only bitcoin
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

#Reverse the order of the df
btc = btc.iloc[::-1].reset_index(drop=True)

#Save df to csv
pd.DataFrame.to_csv(btc, 'D:\Python\coins\Bitcoin.csv', sep=',', index='Date')

#Table with 200 coins (Load more button prevents to scrape more)
url = 'https://coinmarketcap.com/all/views/all/'
response = requests.get(url)
response.status_code
response.content
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find_all('table')[2]
len(table) #page has 3 tables, but we extract only the main one, with the values
#Scrape the whole table (200 coins)
for row in table.find_all('tr'):
    for cell in row.find_all('td'):
        print(cell.text)
#Save the result in the txt file
with open ('200Coins.txt', 'w') as r:
    for row in table.find_all('tr'):
        for cell in row.find_all('td'): 
            r.write(cell.text.ljust(25))
        r.write('\n')

#All coins
num = 1
while num < 38: #38 pages in sum to scrape
    url = 'https://coinmarketcap.com/{}'.format(num) 
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_ = "cmc-table cmc-table___11lFC cmc-table-homepage___2_guh")
        with open ('AllCoins.txt', 'a') as r:
            for row in table.find_all('tr'):
                for cell in row.find_all('td'): 
                    r.write(cell.text.ljust(20))
                r.write('\n')
    else:
        print('No response')
        print(num)              
    num += 1 
    
