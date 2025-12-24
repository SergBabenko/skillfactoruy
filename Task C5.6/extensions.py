import json
import requests
from config import keys, headers


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты {base}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}!')

        r = requests.get(
            f"https://api.apilayer.com/currency_data/convert?to={quote_ticker}&from={base_ticker}&amount={amount}",
            headers=headers)
        total_base = json.loads(r.content)['result']

        return total_base