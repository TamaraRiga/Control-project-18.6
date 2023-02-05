# классы для работы бота по конвертации валюты
import requests
import json
from config import keys


class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(val_origin: str, val_base: str, amount: str):
        if val_origin == val_base:
            raise APIException(f'А вам точно надо менять {val_origin} на {val_base}?')

        try:
            val_origin_ticker = keys[val_origin]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {val_origin}')

        try:
            val_base_ticker = keys[val_base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {val_base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={val_origin_ticker}&tsyms={val_base_ticker}')
        total_base = json.loads(r.content)[keys[val_base]]

        return total_base

