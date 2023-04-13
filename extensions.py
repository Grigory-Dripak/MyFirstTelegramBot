import requests
import json
import xml.etree.ElementTree as ET
from os import getenv
from dotenv import load_dotenv, find_dotenv

class CurrencyConverter:
    url_cbr = 'https://cbr.ru/scripts/XML_daily.asp'
    url_apilayer = 'https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=EUR,USD'
    legal_currency = dict(USD='доллар',
                          EUR='евро',
                          RUB='рубль')

    def get_price(self, base: str, quote: str, amount: float, key):
        pass

    def get_apidata(self):
        load_dotenv(find_dotenv())
        req = json.loads(requests.get(self.url_apilayer, {'apikey': getenv('APIKEY')}).content)

        with open('apilayer_dict.json', 'w') as file:
            json.dump(req, file, indent=4, ensure_ascii=False)

    def get_cbrdata(self):
        cbr = requests.get(self.url_cbr)
        cbr.encoding = 'windows-1251'
        tree = ET.fromstringlist(cbr)
        cbr_date = tree.get('Date')
        cur_id = tree.findall('Valute/CharCode')
        cur_value = tree.findall('Valute/Value')
        cur_values = {}
        for i in range(len(cur_id)):
            if cur_id[i].text in self.legal_currency:
                cur_values[cur_id[i].text]=cur_value[i].text.replace(',', '.')

        with open('cbr_data.txt', 'w') as file:
            for i, j in cur_values.items():
                file.write(f"Курс ЦБ от {cbr_date}: {i}={j}\n")
