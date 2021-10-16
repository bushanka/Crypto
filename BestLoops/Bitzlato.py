import datetime
import random
import time
import requests
from jose import jws
from jose.constants import ALGORITHMS
import json
import pprint

# secret user key
key = {"kty": "EC",
       "alg": "ES256",
       "crv": "P-256",
       "x": "KEY",
       "y": "EXAMPLE",
       "d": "EXAMPLE"} # ключи изменены


def parse_bz(pay_method='Sberbank', order_type='purchase', cryptocurrency='BTC'):
    dt = datetime.datetime.now()
    ts = time.mktime(dt.timetuple())
    claims = {
        # user identificator
        "email": "bushanka2805@gmail.com",
        # leave as is
        "aud": "usr",
        # token issue time
        "iat": int(ts),
        # unique token identificator
        "jti": hex(random.getrandbits(64))
    }
    # make token with claims from secret user key
    token = jws.sign(claims, key, headers={"kid": "1"}, algorithm=ALGORITHMS.ES256)

    currency = 'RUB'

    if pay_method == "Tinkoff":
        pay_method_id = 443
    elif pay_method == 'Sberbank':
        pay_method_id = 3547
    else:
        pay_method_id = 443

    r = requests.get('https://bitzlato.com/api/p2p/exchange/dsa/', headers={
        "Authorization": "Bearer " + token
    },
                     params={
                         "cryptocurrency": f'{cryptocurrency}',
                         "currency": f"{currency}",
                         "type": f"{order_type}",  # purchase, selling
                        # "isOwnerActive": True,
                        # "isOwnerVerificated": True,
                         "limit": 20,
                         "paymethod": f'{pay_method_id}'
                     })
    return json.loads(r.text)


if __name__ == '__main__':
    a = parse_bz()
    pprint.pprint(a['data'])
