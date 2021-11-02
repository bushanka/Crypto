import requests
import json
import time


def binance_p2p_parser(coin='USDT', trade_type='BUY', page=1, payTypes='Tinkoff'):
    data = {"asset": coin.upper(), "fiat": "RUB", "page": page, "payTypes": [p for p in payTypes.split()],
            "publisherType": None, "rows": 20, "tradeType": trade_type}
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
   # proxies = {'https':'184.155.36.194:8080', 'http':'184.155.36.194:8080'}

    # Запрос первой страницы
    r = requests.post('https://fapi.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=data)
    try:
        to_iter = {page: json.loads(r.text)}
    except:
        time.sleep(60)
        r = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=data)
        to_iter = {page: json.loads(r.text)}

    # Добавить {data['asset'].lower(): если не тестим main2
    return [{'nickName': dicts["advertiser"]["nickName"], 'price': dicts["adv"]["price"],
             'fiatSymbol': dicts["adv"]["fiatSymbol"],
             'minAmount': dicts["adv"]["minSingleTransAmount"],
             'maxAmount': dicts["adv"]["dynamicMaxSingleTransAmount"],
             'paymentMethod': [met["tradeMethodName"] for met in dicts['adv']['tradeMethods']],
             'numberOfDeals': dicts["advertiser"]["monthOrderCount"],
             'userType': dicts["advertiser"]["userType"]} for dicts in  to_iter[1]['data']]  # for n in range(1, total_pages, 1) - это если парсим n страниц


def parse_rub():
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }

    # Затем проверяем можно ли купить баланс биржы за 0.99 р
    data_rub = {"asset": "RUB", "fiat": "RUB", "page": 1, "payTypes": [], "publisherType": None, "rows": 10,
                "tradeType": 'BUY'}
    rub_req = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers,
                            json=data_rub)
    tex = json.loads(rub_req.text)
    # pprint.pprint(tex)
    return tex['data'][0]['adv']['price']


if __name__ == '__main__':
    pprint.pprint(binance_p2p_parser(coin='eth', trade_type='SELL'))
