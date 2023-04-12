import requests
import xml.etree.ElementTree as ET

class CurrencyConverter:
    url_cbr = 'https://cbr.ru/scripts/XML_daily.asp'
    url_apilayer = 'https://api.apilayer.com/exchangerates_data/'

tree = ET.fromstringlist(cbr)
c = tree.findall('Valute/CharCode')
v = tree.findall('Valute/Value')
cbr_date = tree.get('Date')
cur_values = {}
for i in range(len(c)):
    if c[i].text in config.legal_currency:
        cur_values[c[i].text]=v[i].text.replace(',', '.')

print(tree)
print(cbr.content)
print(cur_values['USD'])
print(cur_values['CNY'])
print(round(float(cur_values['USD'])/float(cur_values['CNY']), 4))
print(cbr_date)


url = 'https://api.apilayer.com/exchangerates_data/'

def get_data(url):
    apilayer_key = {'apikey': 'HPZdNuGf6xt3PNnHxlzAM0wIWUyXGm7I'}
    req = requests.get(url, apilayer_key)
    req.encoding = 'windows-1251'

    with open('apilayer_data.txt', 'w') as file:
        file.write(req.text)

currencies = []

for c in legal_currency.keys():
    if c != 'RUB':
        currencies.append(c)
currencies = ','.join(currencies)

get_data(f'{url}latest?base=RUB&symbols={currencies}')