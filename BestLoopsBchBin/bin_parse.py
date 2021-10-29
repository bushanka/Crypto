from binance.client import Client

api_key = 'CWGUCrd8vlO0LxcETIHNREHvkYionvrsjVBI8cebz1FJeZbxRFf4RAMtHu50lNT6'
api_secret = '27EQ7gSL8EskW338q5uh0Wk3DibCp5ZceLsfzTR2Gp803gLAaANz3Pb5ouPQLz0F'

client = Client(api_key, api_secret)
ALL_COIN_NAMES = [cur['coin'] for cur in client.get_all_coins_info()] + ["RUB"]
ALL_COIN_NAMES_D = {cur['coin']: 0 for cur in client.get_all_coins_info()}

def legacy_find_all_pairs(ticker, all_tickers):  # TODO не использовать больше эту функцию
    ans = []
    price_tik = []
    for pairs_dict in all_tickers:
        if ticker in pairs_dict['symbol']:
            price_tik.append(pairs_dict)
            ans.append(pairs_dict['symbol'].replace(ticker, ''))
    return ans, price_tik


# TODO Работает долго, около 3.5 сек на все пары с рублем
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


# TODO Работает долго, около 3.5 сек на все пары с рублем
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

# TODO не находит то что видит версия 2
def split_ticker_legacy(ticker_symbol):
    for i in range(len(ticker_symbol)):
        s1 = ticker_symbol[0:len(ticker_symbol) // 2 + i * (-1) ** (i + 1)]
        s2 = ticker_symbol[len(ticker_symbol) // 2 + i * (-1) ** (i + 1)::]
        if s1 in ALL_COIN_NAMES and s2 in ALL_COIN_NAMES:
            return s1, s2
    return None, None

def split_ticker(ticker_symbol):
    for i in range(len(ticker_symbol)):
        # s1 = ticker_symbol[0:len(ticker_symbol) // 2 + i%2 * (-1) ** (i + 1)]
        # s2 = ticker_symbol[len(ticker_symbol) // 2 + (i+1)%2 * (-1) ** (i + 1)::]
        s1 = ticker_symbol[0:2+i]
        s2 = ticker_symbol[2+i::]
        try:
            ALL_COIN_NAMES_D[s1]
            ALL_COIN_NAMES_D[s2]
            return s1, s2
        except:
            pass
    return None, None

# Медленнее чем версия 1, но находит все пары
def split_ticker_2_legacy(ticker_symbol):
    for i in range(len(ticker_symbol)):
        s1 = ticker_symbol[0:2 + i]
        s2 = ticker_symbol[i + 2::]
        if s1 in ALL_COIN_NAMES and s2 in ALL_COIN_NAMES:
            return s1, s2
    return None, None


if __name__ == '__main__':
    t = 'BTCETH'
    print(split_ticker_(t), split_ticker(t))
    # import re
    # from best_change_parser import read_data
    #
    #
    # def decode_BCH_ticker(ticker):
    #     m = re.search('\((.+?)\)', ticker)
    #     if m:
    #         return (m.group(1))
    #     return ticker
    #
    #
    # rub_rates = {}
    # ALL_TICKERS = client.get_orderbook_tickers()
    # rub_table = find_all_pairs_ca('RUB', ALL_TICKERS)  # бинансовская таблица
    # all_rates = read_data()  # бч
    # ruble_source_list = ["QIWI RUB", "Тинькофф", "Сбербанк"]
    #
    # for rate in all_rates:
    #     for rub_source in ruble_source_list:
    #         if rate['id_currency_give_away'] == rub_source:
    #             if decode_BCH_ticker(rate['id_currency_get']) in rub_rates:
    #                 if rate['id_currency_give_away'] in rub_rates[decode_BCH_ticker(rate['id_currency_get'])]:
    #                     rub_rates[decode_BCH_ticker(rate['id_currency_get'])][rate['id_currency_give_away']].append(
    #                         rate)
    #                 else:
    #                     rub_rates[decode_BCH_ticker(rate['id_currency_get'])][rate['id_currency_give_away']] = [rate]
    #             else:
    #                 rub_rates[decode_BCH_ticker(rate['id_currency_get'])] = {rate['id_currency_give_away']: [rate]}
    #
    # ALL_TICKERS = client.get_orderbook_tickers()
    #
    # import time
    #
    # start_time = time.time()
    # for medium_cur in rub_rates.keys():
    #     medium_cur_table = find_all_pairs_ca(medium_cur, ALL_TICKERS)
    # print("--- %s seconds ---" % (time.time() - start_time))
