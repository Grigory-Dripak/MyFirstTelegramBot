import requests
import json
import xml.etree.ElementTree as ET
from time import time, strftime, localtime
from os import getenv
from dotenv import load_dotenv, find_dotenv

class CurrencyConverter:

    def __init__(self):
        self.url_cbr = 'https://cbr.ru/scripts/XML_daily.asp'
        self.url_apilayer = 'https://api.apilayer.com/exchangerates_data/convert?'
        self.legal_currency = ['USD', 'EUR', 'RUB']
        self.get_cbrdata()

    def get_price(self, base: str, quote: str, amount: float):
        load_dotenv(find_dotenv())
        url = f'{self.url_apilayer}to={quote}&from={base}&amount={amount}'
        api = json.loads(requests.get(url, {'apikey': getenv('APIKEY')}).content)
        yy, mm, dd = f"{api['date']}".split('-')

        text = f'По данным Apilayer на {dd}.{mm}.{yy}: {amount} {base} = {api["result"]} {quote} ' \
               f'по курсу {api["info"]["rate"]}'

        #добавляем информацию по курсам от ЦБ РФ
        if strftime('%d.%m.%Y ', localtime(time())) != self.timecbrload:
            self.cbr_cvalues.clear()
            self.get_cbrdata()

        if base == 'RUB':
            cbr_result = round(amount / float(self.cbr_cvalues[quote]), 2)
            cbr_rate = round(1 / float(self.cbr_cvalues[quote]), 5)
        elif quote == 'RUB':
            cbr_result = round(amount * float(self.cbr_cvalues[base]), 2)
            cbr_rate = self.cbr_cvalues[base]
        else:
            cbr_result = round(amount * float(self.cbr_cvalues[base]) / float(self.cbr_cvalues[quote]), 2)
            cbr_rate = round(float(self.cbr_cvalues[base]) / float(self.cbr_cvalues[quote]), 5)

        text += f'\n По данным ЦБ РФ на {self.cbr_date}:  {amount} {base} = {cbr_result} {quote} ' \
                f' по курсу {cbr_rate}'

        return text


    def get_cbrdata(self):
        cbr = requests.get(self.url_cbr)
        cbr.encoding='windows-1251'
        tree = ET.fromstringlist(cbr)
        self.cbr_date = tree.get('Date')
        cur_id = tree.findall('Valute/CharCode')
        cur_value = tree.findall('Valute/Value')
        self.cbr_cvalues = {}
        for i in range(len(cur_id)):
            if cur_id[i].text in self.legal_currency:
                self.cbr_cvalues[cur_id[i].text] = cur_value[i].text.replace(',', '.')
        self.timecbrload = strftime('%d.%m.%Y ', localtime(time()))

