import re
#import time
from binance.client import Client
api_key = 'CWGUCrd8vlO0LxcETIHNREHvkYionvrsjVBI8cebz1FJeZbxRFf4RAMtHu50lNT6'
api_secret = '27EQ7gSL8EskW338q5uh0Wk3DibCp5ZceLsfzTR2Gp803gLAaANz3Pb5ouPQLz0F'
client = Client(api_key, api_secret)

import pandas as pd

from best_change_parser import read_data
from bin_parse import find_all_pairs_bc, find_all_pairs_ca

from aiogram.utils.markdown import hlink


def extract_dat(dat_path):
    data = pd.read_csv(dat_path, encoding='windows-1251')
    return data


def lowest_price_in_list(list_of_rs):
    best_offer = {'course_give_away': '10000000000000000'}
    for offer in list_of_rs:
        if float(offer['course_give_away']) < float(best_offer['course_give_away']):
            best_offer = offer
    return best_offer


def prof(buy_p, sell_p):
    return float(sell_p) / float(buy_p) * 100 - 100


BLACK_LIST = ['Наличные', 'Perfect Money', 'UNI RUB']


def check_BL(offer):
    for elem in BLACK_LIST:
        if elem in offer['id_currency_get']:
            return False
    return True


def decode_BCH_ticker(ticker):
    m = re.search('\((.+?)\)', ticker)
    if m:
        return (m.group(1))
    return ticker


def pair_to_link(token_a, token_b):
    m1 = token_a.find(" (")
    m2 = token_b.find(" (")
    code1 = token_a[0:m1].lower().replace(" ", "-")
    code2 = token_b[0:m2].lower().replace(" ", "-")
    if token_a == "QIWI RUB":
        code1 = 'qiwi'
    if token_a == "Тинькофф":
        code1 = 'tinkoff'
    if token_a == "Сбербанк":
        code1 = 'sberbank'
    return "https://www.bestchange.ru/{}-to-{}.html".format(code1, code2)


def start_parse_bch():
   # start_time = time.time()
    ALL_TICKERS = client.get_orderbook_tickers()
   # print("--- %s seconds --- to download BINANCE files" % (time.time() - start_time))

    # print(pair_to_link("QIWI RUB", "Tether TRC20 (USDT)"))
    min_percent = 0.4
    rub_table = find_all_pairs_ca('RUB', ALL_TICKERS)  # бинансовская таблица
    all_rates = read_data()  # бч
    ruble_source_list = ["QIWI RUB", "Тинькофф", "Сбербанк"]
    rub_rates = {}
    ans_a = []
    ans_b = []
    # print("Let's go")
    for rate in all_rates:
        for rub_source in ruble_source_list:
            if rate['id_currency_give_away'] == rub_source:
                if decode_BCH_ticker(rate['id_currency_get']) in rub_rates:
                    if rate['id_currency_give_away'] in rub_rates[decode_BCH_ticker(rate['id_currency_get'])]:
                        rub_rates[decode_BCH_ticker(rate['id_currency_get'])][rate['id_currency_give_away']].append(
                            rate)
                    else:
                        rub_rates[decode_BCH_ticker(rate['id_currency_get'])][rate['id_currency_give_away']] = [rate]
                else:
                    rub_rates[decode_BCH_ticker(rate['id_currency_get'])] = {rate['id_currency_give_away']: [rate]}
    cross_currents = list(set(rub_table.keys()) & set(rub_rates.keys()))
    a_level_paths = []
    messages = []

    for cur in cross_currents:
        for payment_method in rub_rates[cur].keys():
            best_offer = lowest_price_in_list(rub_rates[cur][payment_method])
            if prof((float(best_offer['course_give_away']) * (1 + 0.001)), rub_table[cur][0], ) > min_percent:
                a_level_paths.append({
                    'exchange_name': best_offer['id_exchange'],
                    'give': best_offer['id_currency_give_away'],
                    'get': best_offer['id_currency_get'],
                    'buy_rate': best_offer['course_give_away'],
                    'sell_rate': rub_table[cur][1],
                    'profit': prof(best_offer['course_give_away'], rub_table[cur][0])})
    a_level_sorted = sorted(a_level_paths, key=lambda k: k['profit'], reverse=True)
    for schemes in a_level_sorted:
        link_text = hlink(schemes['exchange_name'],
                          pair_to_link(schemes['give'], schemes['get']))
        messages.append(
            "[{}] {} -> {} -> RUB\n\nBestChange: {}\n\nBinance: {}\n\nСпред {:.3f} %".format(
                link_text,
                schemes['give'],
                schemes['get'],
                schemes['buy_rate'],
                schemes['sell_rate'],
                prof(schemes['buy_rate'], schemes['sell_rate'])))

    for m in messages:
        ans_a.append(m)
    #  начинаме построение коридоров уровня бэ. по=хорошему надо сделать рекурсивно
    #
    b_level = []
    b_messages = []
    for medium_cur in rub_rates.keys():
        medium_cur_table = find_all_pairs_bc(medium_cur, ALL_TICKERS)
        possible_currents = list(set(cross_currents) & set(find_all_pairs_ca(medium_cur, ALL_TICKERS).keys()))  # CHANGED
        for payment_method in rub_rates[medium_cur]:
            best_offer = lowest_price_in_list(rub_rates[medium_cur][payment_method])
            for final_cur in possible_currents:
                final_rate = float(best_offer['course_give_away']) * (
                        medium_cur_table[final_cur][0] * (1 + 0.002))  # APPROX
                if prof(final_rate, rub_table[final_cur][0]) > min_percent:
                    b_level.append({'exchange_name': best_offer['id_exchange'],
                                    'give': best_offer['id_currency_give_away'],
                                    'get': best_offer['id_currency_get'],
                                    'buy_rate': best_offer['course_give_away'],

                                    'binance_coin_sell': medium_cur,
                                    'binance_coin_buy': final_cur,
                                    'medium_rate': medium_cur_table[final_cur][1],
                                    'sell_rate': rub_table[final_cur][1],

                                    'profit': prof(final_rate, rub_table[final_cur][0])})

    b_level_sorted = sorted(b_level, key=lambda k: k['profit'], reverse=True)
    for schemes in b_level_sorted:
        link_text = hlink(schemes['exchange_name'],
                          pair_to_link(schemes['give'], schemes['get']))
        b_messages.append(
            "[{}] {} -> {} -> {} -> RUB\n\nBestChange: {}\n\nBinance {}-{}: {}\n\nBinance "
            "{}-RUB: {}\n\nСпред {:.3f} %".format(
                link_text,
                schemes['give'],
                schemes['get'],
                schemes['binance_coin_buy'],
                schemes['buy_rate'],
                schemes['get'],
                schemes['binance_coin_buy'],  # decode here
                schemes['medium_rate'],
                schemes['binance_coin_buy'],
                schemes['sell_rate'],
                schemes['profit']))
    for bm in b_messages:
        ans_b.append(bm)
    return ans_a, ans_b


if __name__ == '__main__':
    msg = start_parse_bch()
    for i in msg[1]:
        print(i)
        print('____')