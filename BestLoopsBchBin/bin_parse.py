from binance.client import Client

api_key = 'CWGUCrd8vlO0LxcETIHNREHvkYionvrsjVBI8cebz1FJeZbxRFf4RAMtHu50lNT6'
api_secret = '27EQ7gSL8EskW338q5uh0Wk3DibCp5ZceLsfzTR2Gp803gLAaANz3Pb5ouPQLz0F'

client = Client(api_key, api_secret)
ALL_COIN_NAMES = [cur['coin'] for cur in client.get_all_coins_info()] + ["RUB"]

# for i in range(len(ALL_TICKERS)):
#     if ALL_TICKERS[i]['symbol'] == "ETHRUB":
#         ALL_TICKERS[i]['askPrice'] = "10000000000000"
#         ALL_TICKERS[i]['bidPrice'] = "10000000000000"

#print("BINANCE downloaded")


def legacy_find_all_pairs(ticker, all_tickers):  # TODO не использовать больше эту функцию
    ans = []
    price_tik = []
    for pairs_dict in all_tickers:
        if ticker in pairs_dict['symbol']:
            price_tik.append(pairs_dict)
            ans.append(pairs_dict['symbol'].replace(ticker, ''))
    return ans, price_tik


def find_all_pairs_ca(coin, tickers):
    result = {}
    for ticker in tickers:
        coin_a, coin_b = split_ticker(ticker['symbol'])
        if not (float(ticker['bidQty']) == 0 or float(ticker['askQty']) == 0):
            if coin == coin_a:
                result[coin_b] = (1 / float(ticker['askPrice']), float(ticker['askPrice']))
            elif coin == coin_b:
                result[coin_a] = (float(ticker['bidPrice']), float(ticker['bidPrice']))
    return result


def find_all_pairs_bc(coin, tickers):
    result = {}
    for ticker in tickers:
        coin_a, coin_b = split_ticker(ticker['symbol'])
        if not (float(ticker['bidQty']) == 0 or float(ticker['askQty']) == 0):
            if coin == coin_a:
                result[coin_b] = (1 / float(ticker['bidPrice']), float(ticker['bidPrice']))
            elif coin == coin_b:
                result[coin_a] = (float(ticker['askPrice']), float(ticker['askPrice']))
    return result


def split_ticker(ticker_symbol):
    for i in range(len(ticker_symbol)):
        s1 = ticker_symbol[0:len(ticker_symbol) // 2 + i * (-1) ** (i + 1)]
        s2 = ticker_symbol[len(ticker_symbol) // 2 + i * (-1) ** (i + 1)::]
        if s1 in ALL_COIN_NAMES and s2 in ALL_COIN_NAMES:
            return s1, s2
    return None, None


if __name__ == '__main__':
    cs = client.get_all_coins_info()
    l1, s1 = legacy_find_all_pairs('RUB', ALL_TICKERS)
    print(len(s1), s1)
    f = find_all_pairs_bc("RUB", ALL_TICKERS)
    print(len(f), f)
