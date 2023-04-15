import requests
import json
import xml.etree.ElementTree as ET
from time import time, strftime, localtime
from os import getenv
from dotenv import load_dotenv, find_dotenv

url_cbr = 'https://cbr.ru/scripts/XML_daily.asp'
url_apilayer = 'https://api.apilayer.com/exchangerates_data/convert?'
legal_currency = ['USD', 'EUR', 'RUB']

class CurrencyConverter:

    def __init__(self):
        self.get_cbrdata()

    def get_price(self, base: str, quote: str, amount: float):
        load_dotenv(find_dotenv())
        url = f'{url_apilayer}to={quote}&from={base}&amount={amount}'
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
        cbr = requests.get(url_cbr)
        cbr.encoding = 'windows-1251'
        tree = ET.fromstringlist(cbr)
        self.cbr_date = tree.get('Date')
        cur_id = tree.findall('Valute/CharCode')
        cur_value = tree.findall('Valute/Value')
        self.cbr_cvalues = {}
        for i in range(len(cur_id)):
            if cur_id[i].text in legal_currency:
                self.cbr_cvalues[cur_id[i].text] = cur_value[i].text.replace(',', '.')
        self.timecbrload = strftime('%d.%m.%Y ', localtime(time()))

    @staticmethod
    def textnormalize(text: str):

        usertext = list(map(lambda x: x.upper(), text.split(' ')))

        if len(usertext) != 3:
            raise APIException('Ошибка в наборе пареметров: введите три параметра через пробел')

        if usertext[0] not in legal_currency:
            raise APIException(f'Валюта {usertext[1]} задана некорректно')

        if usertext[1] not in legal_currency:
            raise APIException(f'Валюта {usertext[1]} задана некорректно')

        if usertext[0] == usertext[1]:
            raise APIException(f'Невозможна конвертация одинаковых валют {usertext[0]}')

        try:
            usertext[2] = float(usertext[2])
        except ValueError:
            raise APIException(f'Параметр количества валюты неверный - конвертация невозможна')

        return usertext


class APIException(Exception):
    pass