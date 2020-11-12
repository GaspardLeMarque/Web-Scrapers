from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

##############################Exploratory section#############################

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
content = soup.find('thead')
for i in content.findAll('p'):
    print(i.text)
    
#List all the available rows     
content = soup.find("tbody")
for i in content.findAll('p'):
    print(i.text)

#Return browser-like version of the page to narrow the search
print(soup.prettify())

###########################Extract only bitcoin###############################

response = requests.get('https://coinmarketcap.com/currencies/'+
                        'bitcoin/historical-data/?start=20130429&end=20201022')
soup = BeautifulSoup(response.content, 'html.parser')
page_data = soup.find('script', id='__NEXT_DATA__', type="application/json")
coin_data = json.loads(page_data.contents[0])
quotes = coin_data['props']['initialState']['cryptocurrency']['ohlcvHistorical']['1']['quotes']

timestamp = []
p_open = []
p_close = []
p_high = []
p_low = []
volume = []
mcap = []

for i in quotes:
    timestamp.append(i['quote']['USD']['timestamp'])
    p_open.append(i['quote']['USD']['open'])
    p_high.append(i['quote']['USD']['high'])
    p_low.append(i['quote']['USD']['low'])
    p_close.append(i['quote']['USD']['close']) 
    volume.append(i['quote']['USD']['volume'])
    mcap.append(i['quote']['USD']['market_cap'])
    
btc = pd.DataFrame(columns = ['Date', 'Open*', 'High', 'Low', 'Close**', 'Volume', 'Market Cap'])    
btc['Date'] = timestamp
btc['Open*'] = p_open
btc['High'] = p_high
btc['Low'] = p_low
btc['Close**'] = p_close
btc['Volume'] = volume
btc['Market Cap'] = mcap

#Shift the index
btc.index += 1 

#Save df to csv
pd.DataFrame.to_csv(btc, 'D:\Python\coins\Bitcoin.csv', sep=',', index='Date')

##############################################################################
###############################OPTIONAL SECTION###############################
##############################################################################

#Table with 200 coins ("Load More" button prevents to scrape all the coins)
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

#Table with all coins in the txt file
num = 1
while num < 39: #38 pages in sum to scrape
    url = 'https://coinmarketcap.com/{}'.format(num) 
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_ = "cmc-table cmc-table___11lFC cmc-table-homepage___2_guh")
        #Save the result in the txt file
        with open ('AllCoins.txt', 'a') as r:
            for row in table.find_all('tr'):
                for cell in row.find_all('td'): 
                    r.write(cell.text.ljust(20))
                r.write('\n')
    else:
        print('No response')
        print(num)              
    num += 1 

#Save names, volumes and mcap into the df
coin_li = []
vol_li = []
mcap_li = []
num = 1
while num < 39:
    url = 'https://coinmarketcap.com/{}'.format(num) 
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_ = "cmc-table cmc-table___11lFC cmc-table-homepage___2_guh")
        for row in table.find_all('tr'):
            for cell in row.find_all('td'):
                for name in cell.find_all('p', class_ = 'Text-sc-1eb5slv-0 iTmTiC'):
                    print(name.text)
                    coin_li.append(name.text)
                for volume in cell.find_all('p', class_ = 'Text-sc-1eb5slv-0 iOrfwG font_weight_500___2Lmmi'):
                    print(volume.text)
                    vol_li.append(volume.text) 
                for mcap in cell.find_all('p', class_ = 'Text-sc-1eb5slv-0 hVAibX'):
                    print(mcap.text)
                    mcap_li.append(mcap.text)    
    else:
        print('No response')
        print(num)              
    num += 1    

VolMcap = pd.DataFrame(list(zip(coin_li, vol_li, mcap_li)), 
               columns =['Name', 'Volume', 'Market Cap'])
VolMcap.index += 1 #shift the index

##############################################################################
########################Extract all coins with the loop#######################
##############################################################################

#Create a dict with all coins IDs and slugs
coins = {}
num = 1
while num < 39:
    url = 'https://coinmarketcap.com/{}'.format(num) 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_data = soup.find('script', id='__NEXT_DATA__', type="application/json")
    #Save all the rows in the JSON format
    coin_data = json.loads(page_data.contents[0]) #.contents[0] removes 'script' tags

    #Create the list of dicts that contains only coins data
    coin_list = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    #Create a dict {'coin ID': 'coin name'}
    for i in coin_list:
        coins[str(i['id'])] = i['slug']
    for i in coin_list:
        print(i['slug'])    
    num += 1   
    
#Save dict to txt file 
with open('coins_slugs.txt', 'w') as file:
     file.write(json.dumps(coins, indent=""))    
    
#Plug-in dict vals to the GET request 
dfs = {} #dict of dataframes
for i in coins: 
    response = requests.get(f'https://coinmarketcap.com/currencies/{coins[i]}/historical-data/?start=20130429&end=20201111')
    print(response)
    if response.status_code == 200:
        print('Scraping ' + i + ' now')    
        time.sleep(10)
        soup = BeautifulSoup(response.content, 'html.parser')
        page_data = soup.find('script', id='__NEXT_DATA__', type="application/json")
#Convert data into json format to operate with the nested dicts        
        coin_data = json.loads(page_data.contents[0])
#Dict with quotes (OHLCV+MCap)        
        quotes = coin_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]['quotes']
#Dict with id, name, symbol and quotes
        info = coin_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]
#Renew the lists for each coin        
        timestamp = []
        p_open = []
        p_high = []
        p_low = []
        p_close = []
        volume = []
        mcap = []
#Scrape columns for each coin
        for j in quotes:
            timestamp.append(j['quote']['USD']['timestamp'])
            p_open.append(j['quote']['USD']['open'])
            p_high.append(j['quote']['USD']['high'])
            p_low.append(j['quote']['USD']['low'])
            p_close.append(j['quote']['USD']['close']) 
            volume.append(j['quote']['USD']['volume'])
            mcap.append(j['quote']['USD']['market_cap'])
#Create dict for each coin        
        quotes_dict = {'Date': timestamp, 
                       'Open*': p_open, 
                       'High': p_high, 
                       'Low': p_low, 
                       'Close**': p_close, 
                       'Volume': volume, 
                       'Market Cap': mcap}
#Create dataframe for each coin
        dfs[i] = pd.DataFrame(quotes_dict, columns = ['Date', 'Open*', 'High', 'Low', 'Close**', 'Volume', 'Market Cap'])
        dfs[i].index += 1 
    else:
        print('No response')
        time.sleep(30)     
