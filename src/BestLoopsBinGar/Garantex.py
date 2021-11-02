import requests


def garantex_parser(coin='usdt'):
    text_file = open("token.txt", "r")
    token = text_file.read()
    text_file.close()
    # print(token)
    host = 'garantex.io'  # Для тестового сервера используйте stage.garantex.biz
    ret = requests.get('https://' + host + '/api/v2/depth',
                       headers={'Authorization': 'Bearer ' + token}, params={'market': coin + 'rub'})
    return ret.json()


if __name__ == '__main__':
    print(garantex_parser())
