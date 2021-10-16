import pandas as pd

from best_change_parser import read_data
from bin_parse import client, find_all_pairs, ALL_TICKERS


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


def start_parse_bch():
    ans = []
    min_percent = 0.4
    rub_table = find_all_pairs('RUB', ALL_TICKERS)
    all_rates = read_data()
    ruble_source_list = ["QIWI RUB", "Тинькофф", "Сбербанк"]
    rub_rates = {}

#    print("Let's go")
    for rate in all_rates:
        for cur in rub_table.keys():
            for rub_source in ruble_source_list:
                if cur in rate['id_currency_get'] and rate['id_currency_give_away'] == rub_source:
                    if cur in rub_rates:
                        rub_rates[cur].append(rate)
                    else:
                        rub_rates[cur] = [rate]

    cross_currents = list(set(rub_table.keys()) & set(rub_rates.keys()))
    a_level_paths = []
    messages = []

    for cur in cross_currents:
        best_offer = lowest_price_in_list(rub_rates[cur])
        if prof((float(best_offer['course_give_away']) * (1 + 0.001)), rub_table[cur], ) > min_percent:
            a_level_paths.append({'give': best_offer['id_currency_give_away'],
                                  'get': best_offer['id_currency_get'],
                                  # 'binance_coin': cur,
                                  'buy_rate': best_offer['course_give_away'],
                                  'sell_rate': rub_table[cur],
                                  'profit': prof(best_offer['course_give_away'], rub_table[cur])})
            messages.append(
                "Обменять {} на\n{} в {}\n\nкурс {}\n\nПродать на Бинансе по курсу {}\n\nПрибыль составит {:.3f} %".format(
                    best_offer['id_currency_give_away'],
                    best_offer['id_currency_get'],
                    best_offer['id_exchange'],
                    best_offer['course_give_away'],
                    rub_table[cur],
                    prof(best_offer['course_give_away'], rub_table[cur])))
    for m in messages:
        ans.append(m)
  #      print(m)
    #  начинаме построение коридоров уровня бэ. по=хорошему надо сделать рекурсивно
    #
    b_level = []
    b_messages = []
    for medium_cur in cross_currents:
        medium_cur_table = find_all_pairs(medium_cur, ALL_TICKERS)
        possible_currents = list(set(cross_currents) & set(medium_cur_table.keys()))
        best_offer = lowest_price_in_list(rub_rates[medium_cur])
        for final_cur in possible_currents:
            final_rate = float(best_offer['course_give_away']) * (medium_cur_table[final_cur] * (1 + 0.002))  # APPROX
            if prof(final_rate, rub_table[final_cur]) > min_percent:
                b_level.append({'give': best_offer['id_currency_give_away'],
                                'get': best_offer['id_currency_get'],
                                'buy_rate': best_offer['course_give_away'],

                                'binance_coin_sell': medium_cur,
                                'binance_coin_buy': final_cur,
                                'medium_rate': medium_cur_table[final_cur],
                                'sell_rate': rub_table[final_cur],

                                'profit': prof(final_rate, rub_table[final_cur])})
                b_messages.append(
                    "Обменять {} на\n{} в {}\n\nкурс: {} \n\nОбменять на Бинансе на {} по курсу {}\n\nПродать по курсу {}\n\nПрибыль составит {:.3f} %".format(
                        best_offer['id_currency_give_away'],
                        best_offer['id_currency_get'],
                        best_offer['id_exchange'],
                        best_offer['course_give_away'],
                        final_cur,
                        medium_cur_table[final_cur],
                        rub_table[final_cur],
                        prof(final_rate, rub_table[final_cur])))
    for bm in b_messages:
        ans.append(bm)
 #       print(bm)
    return ans

if __name__ == '__main__':
    print(start_parse_bch())
