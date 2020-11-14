from bs4 import BeautifulSoup
import requests

#Scrape prices of futures
assets = {'Gold': 'GC=F?p=GC=F', 
          'Silver': 'SI%3DF?p=SI%3DF', 
          'Crude Oil': 'CL=F?p=CL=F'}
prices = []

def GetPrices(symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    url = f'https://finance.yahoo.com/quote/{symbol}'
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    asset = {     
    'symbol': symbol,    
    'price': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[0].text
    }
    return asset

print(GetPrices('SI%3DF?p=SI%3DF')) #GC=F ticker gold futures

for i in assets.values():
    prices.append(GetPrices(i))
print(prices) 
