from BinanceP2P import binance_p2p_parser
from Garantex import garantex_parser
from Bitzlato import parse_bz
import time
import pprint
from code_generator import decode_key
from time import sleep

# Фии
def fee_transfer(coin):
    data_fee = {'btc': 0.0000044, 'eth': 0.000064, 'usdt': 0.8}
    return data_fee[coin]

def fee_transfer_bz(coin):
    data_fee = {'btc': 0.0005, 'eth': 0.003, 'usdt': 20}
    return data_fee[coin]


def parse_all_info():
    pay_types = ['Tinkoff', 'Sberbank']
    coins = ['btc', 'eth', 'usdt']
    trade_types = ['SELL', 'BUY']
    order_t = ['selling']

    parsed_all_binance = {}
    parsed_all_bitzlato = {}

    for types in pay_types:
        parsed_all_binance[types] = [{c: [binance_p2p_parser(c, trade_type=tr, payTypes=types) for tr in trade_types]}
                                     for c in coins]
       # sleep(20)
        parsed_all_bitzlato[types] = [
            {c: [parse_bz(cryptocurrency=c.upper(), pay_method=types, order_type=tr) for tr in order_t]} for c in coins]
    parse_all_gar = {}

    for c in coins:
        parse_all_gar[c] = garantex_parser(c)

    return parsed_all_binance, parse_all_gar, parsed_all_bitzlato


def re_parse_gar():
    pay_types = ['Tinkoff', 'Sberbank']
    coins = ['btc', 'eth', 'usdt']
    trade_types = ['SELL', 'BUY']

    parse_all_gar = {}
    sleep(60)

    for types in pay_types:
        for c in coins:
            parse_all_gar[c] = garantex_parser(c)

    return parse_all_gar


def re_parse_bz():
    pay_types = ['Tinkoff', 'Sberbank']
    coins = ['btc', 'eth', 'usdt']
    order_t = ['selling']

    parsed_all_bitzlato = {}
    sleep(60)

    for types in pay_types:
        parsed_all_bitzlato[types] = [{c: [parse_bz(cryptocurrency=c.upper(), pay_method=types, order_type=tr) for tr in order_t]} for c in coins]

    return parsed_all_bitzlato


# Эту функцию будем вызывать каждый раз после того как спарсим данные
# Для каждого пользователя эта функция вызывается индивидуально 1 раз
# И она должна возвращать массив строчек который нужно отправить пользователю
def filter_param(volume, payment_method, parsed_binance, parsed_gar, parsed_bz, is_binance_usdt, is_binance_eth, is_binance_btc, is_gar_usdt, is_gar_eth, is_gar_btc,
                 is_bz_usdt, is_bz_eth, is_bz_btc, percent=0.5, min_amount=10000):
    send_to_user_info_on_bin_gar = []
    send_to_user_info_on_gar_bin = []
    send_to_user_info_on_bz_gar = []
    send_to_user_info_on_gar_bz = []

    coins = ['btc', 'eth', 'usdt']

    for num, c in enumerate(coins):
        for pay_met, is_pay_meth in payment_method.items():
            # Binance -> Garantex
            try:
                sell_price_on_gar = float(parsed_gar[c]['asks'][0]['price'])  # Здесь краш если код не перегенирирован
            except:
                decode_key()
                parsed_gar = re_parse_gar()
                sell_price_on_gar = float(parsed_gar[c]['asks'][0]['price'])
            if parsed_gar[c] is not None: 
                buy_price_on_binance_p2p = float(parsed_binance[pay_met][num][c][0][-1]['price'])

                for seller in parsed_binance[pay_met][num][c][0]:
                    if seller['numberOfDeals'] >= 30 and float(seller['minAmount']) <= min_amount:
                        buy_price_on_binance_p2p = float(seller['price'])
                        break

                profit = ((volume / (buy_price_on_binance_p2p * 1.001) - fee_transfer(
                    c)) * sell_price_on_gar * 0.9985 - volume) / volume * 100

                if profit > percent and is_pay_meth and ((is_binance_usdt == 1 and c=='usdt') or (is_binance_eth == 1 and c=='eth') or (is_binance_btc and c=='btc')) :
                    send_to_user_info_on_bin_gar.append(
                        f'{c.upper()}\n\n' + 'Цена Binance P2P ' + pay_met +
                        ': \n{:,} ₽\n\n'.format(
                            buy_price_on_binance_p2p) + 'Цена Garantex: \n{:,} ₽\n\n'.format(
                            sell_price_on_gar) + '\n\nВаш нижний лимит: {:,} ₽\n\n'.format(
                            min_amount) + 'Прибыль: {:,.3f} ₽\n\n'.format(
                            (volume / (buy_price_on_binance_p2p * 1.0015) - fee_transfer(
                                c)) * sell_price_on_gar * 0.999 - volume) + 'Процент: {:.3f} %\n\n'.format(profit))
            # Garantex -> Binance
            if parsed_gar[c] is not None:
                buy_price_on_gar = float(parsed_gar[c]['bids'][0]['price'])
                sell_price_on_binance_p2p = float(parsed_binance[pay_met][num][c][1][-1]['price'])

                for seller in parsed_binance[pay_met][num][c][1]:
                    if seller['numberOfDeals'] >= 30 and float(seller['maxAmount']) >= volume:
                        sell_price_on_binance_p2p = float(seller['price'])
                        break
                profit = ((volume / (buy_price_on_gar * 1.0015) - fee_transfer(
                    c)) * sell_price_on_binance_p2p * 0.999 - volume) / volume * 100
                if profit > percent and is_pay_meth and ((is_gar_usdt == 1 and c=='usdt') or (is_gar_eth == 1 and c=='eth') or (is_gar_btc and c=='btc')):
                    send_to_user_info_on_gar_bin.append(f'{c.upper()}\n\n' +
                                                        'Цена Garantex: \n{:,} ₽\n\n'.format(buy_price_on_gar) +
                                                        'Цена Binance P2P ' + pay_met + ': \n{:,} ₽'.format(
                        sell_price_on_binance_p2p) + '\n\nВаш объем: {:,} ₽\n\n'.format(
                        volume) + 'Прибыль: {:,.3f} ₽\n\n'.format(
                        (volume / (buy_price_on_gar * 1.0015) - fee_transfer(
                            c)) * sell_price_on_binance_p2p * 0.999 - volume) + 'Процент: {:.3f} %\n\n'.format(profit))
            # Bitzlato -> Garantex
            if parsed_bz[pay_met][num][c][0] is not None:
                try:
                    parsed_bz[pay_met][num][c][0]['data']
                    bz_to_go = True
                except KeyError:
                    bz_to_go = False
            else:
                bz_to_go = False
            if bz_to_go:
                #try:
                buy_price_on_bz = float(parsed_bz[pay_met][num][c][0]['data'][0]['rate'])
               # except:
                   # parsed_bz = re_parse_bz()
                   # buy_price_on_bz = float(parsed_bz[pay_met][num][c][0]['data'][0]['rate'])
                sell_price_on_gar = float(parsed_gar[c]['asks'][0]['price'])
                # print(parsed_bz[pay_met][num][c][0]['data'])

                for seller in parsed_bz[pay_met][num][c][0]['data']:
                    # print(float(seller['rate']))
                    if float(seller['limitCurrency']['min']) <= min_amount:
                        buy_price_on_bz = float(seller['rate'])
                        # print('!!!!', buy_price_on_bz)
                        break
                profit = ((volume / (buy_price_on_bz * 1.005) - fee_transfer_bz(
                    c)) * sell_price_on_gar * 0.9985 - volume) / volume * 100
                if profit > percent and is_pay_meth and ((is_bz_usdt == 1 and c=='usdt') or (is_bz_eth == 1 and c=='eth') or (is_bz_btc and c=='btc')):
                    send_to_user_info_on_bz_gar.append(f'{c.upper()}\n\n' +
                                                       'Цена Bitzlato ' + pay_met + ': \n{:,} ₽\n\n'.format(
                        buy_price_on_bz) +
                                                       'Цена Garantex: \n{:,} ₽'.format(
                                                           sell_price_on_gar) + '\n\nВаш нижний лимит: {:,} ₽\n\n'.format(
                        min_amount) + 'Прибыль: {:,.3f} ₽\n\n'.format(
                        (volume / (buy_price_on_bz * 1.005) - fee_transfer_bz(
                            c)) * sell_price_on_gar * 0.9985 - volume) + 'Процент: {:.3f} %\n\n'.format(profit))

    return send_to_user_info_on_bin_gar, send_to_user_info_on_gar_bin, send_to_user_info_on_bz_gar


if __name__ == '__main__':
    params = parse_all_info()
    start_time = time.time()
    pprint.pprint(filter_param(volume=100000, payment_method='Sberbank', parsed_binance=params[0], parsed_gar=params[1],
                               parsed_bz=params[2], min_amount=2000))
    print("--- %s seconds ---" % (time.time() - start_time))
