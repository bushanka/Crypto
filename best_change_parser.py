import requests
import zipfile
import pandas as pd


def download_url(url_download, save_path_zip, chunk_size=128):
    """"Загрузка файла для парса"""

    req = requests.get(url_download, stream=True)
    with open(save_path_zip, 'wb') as fd:
        for chunk in req.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def extract_zip(file_path, target_dir):
    """Разархивирует zip-файл"""

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)


def extract_dat(dat_path):
    """Читаем dat-файл и записываем в csv"""

    data = pd.read_csv(dat_path, encoding='windows-1251', header=None)
    return data


def read_data():
    """Запуск всех функций с нужными path'ами, возвращаем что-то типа json"""

    save_path = 'bch_api.zip'
    url = 'http://api.bestchange.ru/info.zip'
    target_directory = 'bch_files'

    download_url(url, save_path)
    extract_zip(save_path, target_directory)

    list_currencies = extract_dat('bch_files/bm_cy.dat')
    list_exch = extract_dat('bch_files/bm_exch.dat')
    list_rates = extract_dat('bch_files/bm_rates.dat')

    curs = {cur_id.split(';')[0]: cur_id.split(';')[2] for cur_id in list_currencies[0]}
    exchangers = {ex_id.split(';')[0]: ex_id.split(';')[1] for ex_id in list_exch[0]}

    # return [{'id_currency': cur_id.split(';')[0], 'name_currency': cur_id.split(';')[2]} for cur_id in
    #         list_currencies[0]], \
    #        [{'id_exchange': ex_id.split(';')[0], 'name_exchange': ex_id.split(';')[1]} for ex_id in
    #         list_exch[0]], \
    #        [{'id_currency_give_away': rates_id.split(';')[0], 'id_currency_get': rates_id.split(';')[1],
    #          'id_exchange': rates_id.split(';')[2], 'course_give_away': rates_id.split(';')[3],
    #          'course_get': rates_id.split(';')[4], 'capacity': rates_id.split(';')[5], 'review': rates_id.split(';')[6]}
    #         for rates_id in list_rates[0]] # Долго сплитит, надо изменять файл dat после загрузки. Замена ;->,

    return [{'id_currency_give_away': curs[rates_id.split(';')[0]],
             'id_currency_get': curs[rates_id.split(';')[1]],
             'id_exchange': exchangers[rates_id.split(';')[2]],
             'course_give_away': rates_id.split(';')[3],
             'course_get': rates_id.split(';')[4],
             'capacity': rates_id.split(';')[5],
             'review': rates_id.split(';')[6]} for rates_id in list_rates[0]]


if __name__ == '__main__':
    r = read_data()
    # print(c, e, sep='\n')
    print(len(r))
    for r_i in r:
        if r_i['id_currency_give_away'] == 'QIWI RUB':
            print(r_i)
