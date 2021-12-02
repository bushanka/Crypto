import re
# import time
from binance.client import Client
import pandas as pd

from best_change_parser import read_data
from bin_parse import find_all_pairs_bc, find_all_pairs_ca

from aiogram.utils.markdown import hlink



api_key = 's4v3IIr7nIRCAO13S1iyM3Yx1sR2X6ExMSxOEnk2cEMiE44QuAxpTNUQI2iRvzTN'
api_secret = 'klkrvk93V8Jns80Ni6s8cWOt0YeU2SVIlDWHc32BEENudMKMTNLlimb2lZaMCLr9'
#client = Client(api_key, api_secret)


def extract_dat(dat_path):
    data = pd.read_csv(dat_path, encoding='windows-1251')
    return data


def lowest_price_in_list(list_of_rs):
    best_offer = {'course_give_away': '10000000000000000', 'id_exchange': None, 'id_currency_give_away': None, 'id_currency_get' : None}
    for offer in list_of_rs:
        if float(offer['course_give_away']) < float(best_offer['course_give_away']) and offer[
            'id_exchange'] not in BLACK_LIST_EX:
            best_offer = offer
    return best_offer


def prof(buy_p, sell_p):
    return float(sell_p) / float(buy_p) * 100 - 100


BLACK_LIST = ['Наличные', 'Perfect Money', 'UNI RUB']
BLACK_LIST_EX = ['ExBox', 'Changelly', 'AvanChange', 'OpenChange', 'МультиВал', 'ImExchanger', 'ExchangeTeam', 'CryptoPay24', 'Quickex', 'FixedFloat', 'Exolix', 'E-Scrooge']
# ХЗ насчет Changelly, может и норм, но заебал спамить в 1 момент

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
    if token_a == "Ether Classic (ETC)":
        code1 = "ethereum-classic"
    if token_b == "Ether Classic (ETC)":
        code2 = "ethereum-classic"
    if token_a == "0x (ZRX)":
        code1 = 'zrx'
    if token_b == "0x (ZRX)":
        code2 = "zrx"
    if token_a == "OmiseGO (OMG)":
        code1 = "omg"
    if token_b == "OmiseGO (OMG)":
        code2 = "omg"
    if token_a == "Binance USD (BUSD)":
        code1 = "busd"
    if token_b == "Binance USD (BUSD)":
        code2 = "busd"

    return "https://www.bestchange.ru/{}-to-{}.html".format(code1, code2)


def filter_params(min_percent, a_level, b_level):
    messages = []
    ans_a = []
    b_messages = []
    ans_b = []

    a_level_sorted = sorted(a_level, key=lambda k: k['profit'], reverse=True)
    for schemes in a_level_sorted:
        if schemes['profit'] > min_percent:
            link_text = hlink(schemes['exchange_name'],
                              pair_to_link(schemes['give'], schemes['get']))
            messages.append(
                {
                    'Text': f"[{link_text}] {schemes['give']} -> {schemes['get']} -> {schemes['give']}"
                            f"\n\nBestChange: {schemes['buy_rate']}\n\nBinance: {schemes['sell_rate']}\n\n"
                            f"Спред {schemes['profit']:.3f} %", 'Paymethod': schemes['paymeth']})

    for m in messages:
        ans_a.append(m)

    b_level_sorted = sorted(b_level, key=lambda k: k['profit'], reverse=True)
    for schemes in b_level_sorted:
        if schemes['profit'] > min_percent:
            link_text = hlink(schemes['exchange_name'],
                              pair_to_link(schemes['give'], schemes['get']))
            b_messages.append(
                {'Text': f"[{link_text}] {schemes['give']} -> {schemes['get']} -> {schemes['binance_coin_buy']} -> "
                         f"{schemes['give']}\n\nBestChange: {schemes['buy_rate']}\n\nBinance"
                         f" {schemes['get']}-{schemes['binance_coin_buy']}: {schemes['medium_rate']}\n\nBinance "
                         f"{schemes['binance_coin_buy']}-{schemes['give']}: {schemes['sell_rate']}\n\n"
                         f"Спред {schemes['profit']:.3f} %", 'Paymethod': schemes['paymeth']})
    for bm in b_messages:
        ans_b.append(bm)
    return ans_a, ans_b


init_points = {'ETH': ['Ethereum (ETH)'],
               'RUB': ["QIWI RUB", "Тинькофф", "Сбербанк"],
               'USDT': ["Tether Omni (USDT)", "Tether TRC20 (USDT)", "Tether BEP20 (USDT)"], # "Tether ERC20 (USDT)"
               'USDC': ["USDC"],
               'TUSD': ["TrueUSD"],
               'USDP': ["Pax Dollar"],
               'DAI': ["Dai"],
               'BUSD': ["Binance USD (BUSD)"],
               'TRX': ['TRON (TRX)'],
               'XLM': ['Stellar (XLM)'],
               'DOGE': ['Dogecoin'],
               'ZEC': ['Zcash (ZEC)'],
               'BTC': ['Bitcoin (BTC)']}


def start_parse_bch(token, sources, ALL_TICKERS, BCH_DATA):
    rub_table = find_all_pairs_ca(token, ALL_TICKERS)  # бинансовская таблица
    all_rates = BCH_DATA  # бч
    ruble_source_list = sources
    rub_rates = {}

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
    a_level = []
    for cur in cross_currents:
        for payment_method in rub_rates[cur].keys():
            if payment_method == 'QIWI RUB':
                pay = 0
            elif payment_method == 'Тинькофф' or payment_method == 'Сбербанк':
                pay = 1
            else:
                pay = 2
            best_offer = lowest_price_in_list(rub_rates[cur][payment_method])
            a_level.append({
                'paymeth': pay,
                'exchange_name': best_offer['id_exchange'],
                'give': best_offer['id_currency_give_away'],
                'get': best_offer['id_currency_get'],
                'buy_rate': best_offer['course_give_away'],
                'sell_rate': rub_table[cur][1],
                'profit': prof(best_offer['course_give_away'], rub_table[cur][0])})

    #  начинаме построение коридоров уровня бэ. по=хорошему надо сделать рекурсивно
    #
    b_level = []
    for medium_cur in rub_rates.keys():
        medium_cur_table = find_all_pairs_bc(medium_cur, ALL_TICKERS)
        possible_currents = list(
            set(cross_currents) & set(find_all_pairs_ca(medium_cur, ALL_TICKERS).keys()))  # CHANGED
        for payment_method in rub_rates[medium_cur]:
            if payment_method == 'QIWI RUB':
                pay = 0
            elif payment_method == 'Тинькофф' or payment_method == 'Сбербанк':
                pay = 1
            else:
                pay = 2
            best_offer = lowest_price_in_list(rub_rates[medium_cur][payment_method])
            for final_cur in possible_currents:
                final_rate = float(best_offer['course_give_away']) * (
                        medium_cur_table[final_cur][0] * (1 + 0.002))  # APPROX
                b_level.append({'paymeth': pay, 'exchange_name': best_offer['id_exchange'],
                                'give': best_offer['id_currency_give_away'],
                                'get': best_offer['id_currency_get'],
                                'buy_rate': best_offer['course_give_away'],

                                'binance_coin_sell': medium_cur,
                                'binance_coin_buy': final_cur,
                                'medium_rate': medium_cur_table[final_cur][1],
                                'sell_rate': rub_table[final_cur][1],

                                'profit': prof(final_rate, rub_table[final_cur][0])})
    return a_level, b_level


def parse_all_from_bch():
    client = Client(api_key, api_secret)
    all_tick = client.get_orderbook_tickers()
    bch = read_data()
    all_a_level = []
    all_b_level = []
    for point in init_points.items():
        msg = start_parse_bch(point[0], point[1], BCH_DATA=bch, ALL_TICKERS=all_tick)
        all_a_level += msg[0]
        all_b_level += msg[1]
    client.close_connection()
    return all_a_level, all_b_level


if __name__ == '__main__':
    import time

    t1 = time.time()
    a = parse_all_from_bch()
    print(time.time() - t1)
    print(filter_params(0, a_level=a[0], b_level=a[1]))
